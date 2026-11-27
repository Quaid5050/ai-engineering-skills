---
name: data-check
description: "Look at a database safely — read-only sessions with a statement timeout on every call, local by default and shared environments only with explicit OK and a read-only role; schema, counts, integrity, tenant isolation, freshness and gaps, query plans, and verifying a migration or backfill with an expected cohort and control rows — without exposing personal data. Use when answering a data question, checking a migration, or chasing a data bug. Trigger on 'check the data', 'query the database', 'how many rows', 'is the data correct', 'verify the migration', 'explain this query', 'look at the table'."
argument-hint: "[data question, migration to verify, or suspected data bug]"
license: MIT
metadata:
  version: "2.0.0"
---

# Data check

Answer `$ARGUMENTS` by reading the database. Default environment: **local**.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

1. Read `AGENTS.md` / the conventions: how the local database runs, its connection settings, the schema's real table and column names, and the rules for shared environments (who may connect, through which path).
2. Read the schema (`\d`, the information schema, or the migrations) before writing a query; names in this skill are examples.

**Gate:** you know the environment, the access path, and the real names of the tables you will query.

## 1. Environments

| Environment | How | Allowed |
|---|---|---|
| Local | The project's local database (compose file, container, local install) | Read freely. Writing seed or test data: ask first, and touch only rows you create |
| Staging / production / any shared database | Only with the user's explicit OK **per session**, a **read-only role**, through the approved access path | **Read only.** Never writes, never DDL, never long-running scans at peak |

## 2. Read-only by default

- Open every session read-only with a statement timeout, **on every call** — a new connection does not inherit the last one's settings. For example: a read-only default transaction and a 30 s statement timeout as session options, or several queries in one script file run in one session.
- Always `LIMIT` exploratory queries; prefer `count(*)` and aggregates over row dumps.
- Never run `UPDATE`, `DELETE`, DDL or a lock-taking statement outside local, and locally only for your own test rows.

## 3. Personal data

- Never print personal data into the conversation, an issue, a PR or a file: names, emails, phone numbers, addresses, coordinates, tokens, free-text notes, payment details. Aggregate (`count`, `min/max(time)`), bucket or round (coordinates to ~10 km, timestamps to the hour), or compare inside the database.
- IDs and rounded buckets may still identify people. Prefer suppressed/aggregated results with an explicit disclosure policy; do not assume pseudonymization is anonymization.
- Results that are personal data stay out of git and out of the issue tracker.

## 4. Useful checks (adapt names)

```sql
-- Schema and size
SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 20;  -- or the engine's equivalent

-- Applied migrations
SELECT * FROM <migration_history_table> ORDER BY 1 DESC LIMIT 5;

-- Freshness: owners whose latest event is older than the expected interval (count only)
SELECT count(*) FROM owners o
LEFT JOIN (
  SELECT owner_id, max(created_at) AS last_at FROM events GROUP BY owner_id
) t ON t.owner_id = o.id
WHERE o.active = true AND (t.last_at IS NULL OR t.last_at < now() - interval '15 minutes');

-- Gaps per hour for one synthetic test owner
SELECT date_trunc('hour', created_at) AS hour, count(*) FROM events
WHERE owner_id = '<test-uuid>' AND created_at > now() - interval '1 day' GROUP BY 1 ORDER BY 1;

-- Integrity: orphans and range violations
SELECT count(*) FROM memberships m LEFT JOIN workspaces w ON w.id = m.workspace_id WHERE w.id IS NULL;
SELECT count(*) FROM order_lines WHERE quantity <= 0;

-- Isolation: rows whose tenant differs from their parent's tenant
SELECT count(*) FROM order_lines l JOIN orders o ON o.id = l.order_id WHERE l.workspace_id <> o.workspace_id;

-- Query plan: ANALYZE executes the statement; use local synthetic data and no side-effecting functions
EXPLAIN (ANALYZE, BUFFERS) <query>;
```

For plans, seed realistic synthetic volume (10× today's) before judging; a plan on ten rows says nothing.

## 5. Verifying a migration or backfill

1. **Before:** count the rows that should change (the expected cohort) and name control rows that must **not** change.
2. Apply the migration or run the backfill locally.
3. **After:** the affected count matches the cohort; controls are unchanged; no `NULL` where the code now requires a value; constraints and indexes exist; representative plans and measured cost meet the query budget.

**Gate:** cohort and controls are both checked; a matching count alone is not enough.

## 6. Report

The question, the environment, the queries run (no personal results), the numbers, and what they mean — facts separated from interpretation. A data bug found → `investigate-bug` or `file-bug` (lifecycle plugin).

## Rules

- Read-only outside local, always; shared environments only with explicit OK per session.
- No personal data in any output that leaves the database session.
- Never fix data during an investigation; the repair is its own reviewed change.

## Composition

| From | This skill | To |
|---|---|---|
| `add-migration` (this plugin), `investigate-bug`, `incident` (lifecycle), `perf-check`, `analytics-event` (quality) | Safe, read-only answers | `file-bug`, `bugfix` (lifecycle) for a data bug |
