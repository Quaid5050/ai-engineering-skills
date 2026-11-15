# Scheduled jobs by stack

| Stack | Runner / scheduler | One scheduler | Claiming | Pitfalls |
|---|---|---|---|---|
| Django / Python | Celery workers + **one** `celery beat` (or `django-celery-beat`), RQ + rq-scheduler, django-q | Single beat replica; during rolling deploys stop the old beat before starting the new (or a scheduler lock) | `select_for_update(skip_locked=True)` inside `transaction.atomic()` | `acks_late` + visibility timeout shorter than the task → the task runs twice; enqueue with `transaction.on_commit(...)`; `TestCase` needs `captureOnCommitCallbacks(execute=True)` |
| Spring (Java/Kotlin) | `@Scheduled` + **ShedLock**, Quartz (clustered, JDBC store), or a queue (SQS, RabbitMQ) consumer | ShedLock lock per job name; Quartz cluster mode | `SELECT … FOR UPDATE SKIP LOCKED` via JPA native query or jOOQ | `@Transactional` self-invocation skips the transaction; `AFTER_COMMIT` events are lost on a crash — use an outbox table |
| Node | BullMQ (Redis) repeatable jobs, pg-boss (Postgres), Agenda | BullMQ repeatable jobs are deduplicated by key; pg-boss `schedule` is singleton | pg-boss uses `SKIP LOCKED`; BullMQ locks jobs per worker | Unhandled promise rejections kill workers silently — always await and catch at the job boundary |
| .NET | Hangfire (recurring jobs, distributed lock), Quartz.NET (clustered), `BackgroundService` + `PeriodicTimer` for loops | Hangfire's distributed lock per recurring job; Quartz clustering | `FOR UPDATE SKIP LOCKED` via raw SQL or `ExecuteUpdate` with a lease column | Hangfire retries by default (10×) — set attempts explicitly so the job is the one retry owner |
| Platform cron (Kubernetes CronJob, cloud schedulers) | The platform triggers an endpoint or a container | `concurrencyPolicy: Forbid` (Kubernetes) or the platform's single-run setting | Same database claim as above | Missed runs during outages: `startingDeadlineSeconds` and a catch-up query for overdue rows |

A unique sent-ledger works the same everywhere:

```sql
CREATE TABLE notification_sent (
  subject_id uuid NOT NULL,
  kind       text NOT NULL,
  due_at     timestamptz NOT NULL,
  sent_at    timestamptz,
  result     text,
  CONSTRAINT uq_notification_sent UNIQUE (subject_id, kind, due_at)
);
-- insert first; a unique violation means "already handled" → skip
```
