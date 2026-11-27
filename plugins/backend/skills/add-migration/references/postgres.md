# PostgreSQL migration examples

Read this when the target database is PostgreSQL and you are reading generated SQL (§4) or writing raw SQL (§3). Behaviour below is for PostgreSQL 12+ unless a version is named; confirm the project's version before relying on a version-specific rule.

## Which `ALTER TABLE` rewrites, scans or is metadata-only

| Statement | Effect on a large table |
|---|---|
| `ADD COLUMN c int` (nullable, no default) | Metadata only; brief `ACCESS EXCLUSIVE` lock |
| `ADD COLUMN c text DEFAULT 'x'` (constant or other non-volatile default, 11+) | Metadata only; existing rows read the stored default |
| `ADD COLUMN c uuid DEFAULT gen_random_uuid()` / `DEFAULT clock_timestamp()` (**volatile** default) | **Full table rewrite** under `ACCESS EXCLUSIVE`. Add the column nullable, backfill in batches, then set the default for new rows |
| `ALTER COLUMN c SET NOT NULL` | **Full scan** under `ACCESS EXCLUSIVE` to prove no nulls — **skipped** if a validated `CHECK (c IS NOT NULL)` already exists (see below) |
| `ALTER COLUMN c TYPE ...` | Usually a **full rewrite** plus index rebuilds. Exceptions that are metadata-only: binary-coercible changes such as `varchar(50)` → `varchar(100)` or `varchar` → `text`. `int` → `bigint` rewrites |
| `ADD CONSTRAINT ... CHECK (...)` / `FOREIGN KEY` without `NOT VALID` | Full scan while holding the lock (for a foreign key, on both tables) |
| `DROP COLUMN` | Metadata only (space is reclaimed later), but running code must no longer read the column |
| `CREATE INDEX` (not concurrent) | Blocks writes for the whole build |

## Lock and statement timeouts

Set them for the migration session so a blocked `ALTER` fails fast instead of queueing every later query behind its lock request:

```sql
SET lock_timeout = '5s';        -- give up if the lock is not granted quickly
SET statement_timeout = '15min'; -- cap any one statement; tune to the step
```

Run in a retry loop (the migration tool or deploy script retries a lock timeout a few times with a pause). Never raise `lock_timeout` to "make it pass"; find the long transaction that holds the lock instead (`pg_stat_activity`, `pg_locks`).

## Indexes: `CREATE INDEX CONCURRENTLY`

```sql
-- must run outside a transaction block: mark the migration non-transactional in the tool
CREATE INDEX CONCURRENTLY ix_orders_workspace_created
  ON orders (workspace_id, created_at DESC);
```

- It takes longer and does two table scans, but allows reads and writes throughout.
- If it fails (deadlock, unique violation, timeout) it leaves an **`INVALID`** index: `DROP INDEX CONCURRENTLY ix_...;` and retry. Do not use `IF NOT EXISTS` with a retry loop: the retry then "succeeds" and keeps the invalid index. Check with `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`.
- `DROP INDEX CONCURRENTLY` likewise for removals.

## Constraints without a long lock: `NOT VALID` + `VALIDATE`

Supported for **`CHECK` and `FOREIGN KEY`** constraints (and, from PostgreSQL 18, `NOT NULL`). **Not** for `UNIQUE` or `PRIMARY KEY` — those use an index built concurrently (below).

```sql
-- step 1 (fast): new and updated rows are checked from now on
ALTER TABLE order_lines
  ADD CONSTRAINT fk_order_lines_order FOREIGN KEY (order_id) REFERENCES orders (id) NOT VALID;

-- step 2 (separate migration or statement): scans existing rows,
-- holding only SHARE UPDATE EXCLUSIVE, so reads and writes continue
ALTER TABLE order_lines VALIDATE CONSTRAINT fk_order_lines_order;
```

`NOT NULL` without the long scan (before 18, or as a portable pattern):

```sql
ALTER TABLE orders ADD CONSTRAINT ck_orders_placed_at_nn CHECK (placed_at IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT ck_orders_placed_at_nn;
ALTER TABLE orders ALTER COLUMN placed_at SET NOT NULL;   -- uses the validated check, no scan
ALTER TABLE orders DROP CONSTRAINT ck_orders_placed_at_nn;
```

Uniqueness over a large table (after duplicates are repaired, skill §5a):

```sql
CREATE UNIQUE INDEX CONCURRENTLY ux_orders_client_id ON orders (workspace_id, client_id);
ALTER TABLE orders ADD CONSTRAINT uq_orders_client_id UNIQUE USING INDEX ux_orders_client_id;
```

## Expand → migrate → contract: renaming a column

Renaming `orders.note` to `orders.customer_note` while old servers and released clients still read `note`:

1. **Expand** (migration A): `ALTER TABLE orders ADD COLUMN customer_note text;` Code deploy 1 writes both columns and reads `customer_note`, falling back to `note`.
2. **Migrate** (a batched job, not a migration): `UPDATE orders SET customer_note = note WHERE id IN (SELECT id FROM orders WHERE customer_note IS NULL AND note IS NOT NULL LIMIT 5000);` repeated until zero rows, with a pause between batches; verify the count with `data-check`.
3. **Contract** (migration B, after no running code or supported client reads `note`): code deploy 2 stops writing `note`; then `ALTER TABLE orders DROP COLUMN note;`.

Each step is its own PR or clearly marked step, with the next step written down.
