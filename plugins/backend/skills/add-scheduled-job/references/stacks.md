# Scheduled jobs by stack

| Stack | Runner / scheduler | Scheduling coordination | Claiming | Pitfalls |
|---|---|---|---|---|
| Django / Python | Celery workers + **one** `celery beat` (or `django-celery-beat`), RQ + rq-scheduler, django-q | Single beat replica; during rolling deploys stop the old beat before starting the new (or a scheduler lock) | `select_for_update(skip_locked=True)` inside `transaction.atomic()` | `acks_late` + visibility timeout shorter than the task → the task runs twice; persist outbox intent in the transaction; `transaction.on_commit(...)` is only a wake-up; `TestCase` needs `captureOnCommitCallbacks(execute=True)` |
| Spring (Java/Kotlin) | `@Scheduled` + **ShedLock**, Quartz (clustered, JDBC store), or a queue (SQS, RabbitMQ) consumer | ShedLock lock per job name; Quartz cluster mode | Engine-specific atomic claim; PostgreSQL, MySQL 8 and Oracle support `FOR UPDATE SKIP LOCKED` (native query or jOOQ); SQL Server does not (see its adapter below) | `@Transactional` self-invocation skips the transaction; `AFTER_COMMIT` events are lost on a crash — use an outbox table |
| Node | BullMQ (Redis) repeatable jobs, pg-boss (Postgres), Agenda | BullMQ repeatable jobs are deduplicated by key; pg-boss `schedule` is singleton | pg-boss uses `SKIP LOCKED`; BullMQ locks jobs per worker | Unhandled promise rejections kill workers silently — always await and catch at the job boundary |
| .NET | Hangfire (recurring jobs, distributed lock), Quartz.NET (clustered), `BackgroundService` + `PeriodicTimer` for loops | Hangfire's distributed lock per recurring job; Quartz clustering | Provider-specific atomic lease update with affected-row check; PostgreSQL locking syntax is not T-SQL | Hangfire retries by default (10×) — set attempts explicitly so the job is the one retry owner |
| Platform cron (Kubernetes CronJob, cloud schedulers) | The platform triggers an endpoint or a container | `concurrencyPolicy: Forbid` (Kubernetes) or the platform's single-run setting | Same database claim as above | Missed runs during outages: `startingDeadlineSeconds` and a catch-up query for overdue rows |

## Durable intent across stacks

An outbox stores pending intent, not proof of sending. Persist it with the business transaction; use an after-commit callback only as an optional wake-up. A duplicate operation key requires reading state and comparing the payload fingerprint. It must never mean unconditional skip.

Example PostgreSQL schema (adapt types, indexes and constraints to the actual engine):

```sql
CREATE TABLE notification_outbox (
  tenant_id uuid NOT NULL,
  operation_id uuid NOT NULL,
  payload_fingerprint text NOT NULL,
  state text NOT NULL DEFAULT 'pending',
  lease_token uuid,
  lease_until timestamptz,
  next_attempt_at timestamptz NOT NULL,
  attempts integer NOT NULL DEFAULT 0,
  provider_reference text,
  acknowledged_at timestamptz,
  PRIMARY KEY (tenant_id, operation_id),
  CHECK (state IN ('pending', 'leased', 'acknowledged', 'retryable',
                   'uncertain', 'cancelled', 'failed'))
);
```

Claim atomically; acknowledge conditionally on the current lease token. Do not keep a row lock across network I/O. Lease fencing prevents stale local writes, but cannot undo a provider call already in flight. Provider idempotency or reconciliation is required for that window; otherwise expose uncertainty.

Celery `on_commit`, Spring after-commit listeners and analogous callbacks can be lost after commit and before publication. A persisted relay closes that loss window. Quartz clustering or scheduler leadership coordinates triggers, not arbitrary external effects. Kubernetes concurrency policy is not a global downstream exactly-once guarantee.

Source: [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html). Verify the installed scheduler/provider version and its retry/idempotency horizon.

## SQL Server / Azure SQL adapter

Do not translate PostgreSQL claim SQL mechanically. A queue may use a short transaction with `UPDLOCK`, `READPAST` and `UPDATE ... OUTPUT`, but lock granularity, escalation and `READ_COMMITTED_SNAPSHOT` affect correctness and valid hints. `READPAST` skips row and page locks but not table locks, and lock escalation to a table lock defeats it, so test under real load. Validate two real connections under the configured isolation level and crash/reclaim tests. Hold no transaction across provider I/O; compare the lease token on acknowledgement. See [Microsoft table hints](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table).
