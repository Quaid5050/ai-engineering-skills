---
name: add-migration
description: "Change a database schema safely on any stack — design the entity and mapping, keys and UTC timestamps, indexes for every filter, expand → migrate → contract for running servers and released clients, generate the migration, read the generated SQL for table rewrites and long locks, apply and verify locally, and write the rollout and rollback notes. Use when adding or changing tables, columns, indexes or constraints. Trigger on 'change the schema', 'add a table', 'add a column', 'new index', 'migration', 'rename a column', 'drop a column', 'backfill'."
argument-hint: "[what data must be stored and who reads it]"
license: MIT
metadata:
  version: "1.0.0"
---

# Add migration

Make the schema change for `$ARGUMENTS`. If empty, ask what must be stored, who reads it and how much of it there will be.

## 0. Read the project

1. Read `AGENTS.md` / the conventions: the migration tool and its commands, where entities and mappings live, how local databases run, and how migrations are deployed (before the new code, in a job, by hand).
2. Open the matching stack reference in `backend-conventions` (this plugin, its `references/` folder) for the exact commands and the "concurrent index" caveat of that tool.
3. Look at the last few migrations: naming, style, whether raw SQL is used.
4. Ask the size question: how many rows does each touched table have in production (or will it have)? A "large" table (millions of rows, or hot writes) changes every rule below.

**Gate:** you know the tool, the deploy order, and which touched tables are large.

## 1. Design

- Where the entity lives is the **stack's and project's decision** (`backend-conventions` references): some stacks keep a plain domain entity with a separate mapping in persistence; others use one model class as both, with rules as its methods. Follow the project's recorded choice; don't invent a second layer for one table.
- Keys: UUIDs (time-ordered where available). Timestamps with time zone, UTC. Enums as short text. Units in column names.
- Constraints per `backend-conventions` §4: `NOT NULL`, foreign keys with an explicit delete behaviour, unique indexes for uniqueness rules, `CHECK` for ranges, the same constants as the domain.
- **An index for every `WHERE`, `JOIN` and `ORDER BY`** the new queries will run; partial indexes for "active" rows.
- Every row a member may read is reachable through its tenant id, so isolation can be checked.
- Spatial data: one coordinate reference system stated in the column type, a spatial index on any geometry used in a filter. Time-series data: partition by time, index `(owner_id, time DESC)`, retention by policy, no foreign keys from the huge table into big tables if the database recommends against it.
- Retention and deletion: what happens to these rows on account deletion?

## 2. Expand → migrate → contract

Running servers and released clients read the old shape during a deploy. So:

1. **Expand:** add new nullable columns or new tables; code writes both old and new.
2. **Migrate:** backfill in a batched job — not inside the migration.
3. **Contract:** a later change makes the column required or drops the old one, once no running code or supported client reads it.

Never rename or drop in one step. State in the PR which step this change is.

**Gate:** the change is one step of the three, and the next step is written down (issue or PR note).

## 3. Create

Create the migration the project's way: **generated** by the ORM (then produce the SQL for just this migration with the tool's script/preview mode) or **hand-written SQL** (versioned files the tool applies in order) — in both cases you read the final SQL. Use raw SQL for what the tool cannot express (partitioning, retention policies, concurrent index builds) — and check the tool's caveat: concurrent index builds usually need a migration that runs outside a transaction.

## 4. Read the SQL

Reject and rework if you see, on a large table:

- a **table rewrite**: a column type change, `NOT NULL` added without a default on existing rows, a default that is not a constant;
- a **non-concurrent index** build;
- a lock-taking `ALTER` (constraint validation without `NOT VALID` + a separate `VALIDATE`);
- a data backfill inside the migration;
- a drop or rename the running code still reads;
- no down path, and no stated "roll forward instead" reason.

Set a lock timeout for the migration session if the database supports it, so a blocked migration fails instead of queueing all traffic.

**Gate:** you can say, for each statement, what lock it takes and for how long on the largest table.

## 5. Apply and verify locally

1. Start the local database (the project's compose file or test container), apply the migration with the project's command, run the full test suite.
2. Apply **down** (or the documented rollback) once, then up again, if the tool supports it. Tools without down migrations (or projects that roll forward) state the roll-forward fix instead, and the migration is tested on a fresh database in the test suite.
3. `data-check` (this plugin): the tables, columns, constraints and indexes exist; the new queries use the indexes (`EXPLAIN`); counts before/after a backfill match the expected cohort.
4. Integration tests for the new data run against this database.

## 5a. Adding a uniqueness rule over existing data

A unique constraint added to a table that already holds duplicates fails — or, worse, gets added "not valid" and hides them. Order:

1. **Count** the duplicates (`data-check`) and decide the repair rule with the owner (keep oldest, merge, mark).
2. **Repair** in a reviewed, batched job or script (not inside the migration on a large table); re-count to zero.
3. **Build the unique index online** (concurrently, outside a transaction where the database needs it).
4. **Attach the constraint** using that index (or keep the unique index as the rule), then make the code rely on it (map the violation to a conflict/"already exists" result).
5. Test: inserting the duplicate now yields the expected result, and the repaired rows are as decided.

## 6. PR

Include: the generated SQL (or its summary), the lock/rewrite assessment, the expand/migrate/contract step and the next one, the backfill plan, retention/deletion, and rollback (`deploy-check`, lifecycle plugin).

## Rules

- Never edit a migration that has run in a shared environment; add a new one.
- Never backfill inside a migration on a large table.
- Never drop or rename in one step while code or clients read the old shape.
- Destructive changes to shared environments run only with the user's explicit OK.

## Composition

| From | This skill | To |
|---|---|---|
| `add-endpoint`, `implement` (lifecycle) | Safe schema change | `data-check` (this plugin), `deploy-check` (lifecycle), `perf-check` (quality) for new queries on large tables |
