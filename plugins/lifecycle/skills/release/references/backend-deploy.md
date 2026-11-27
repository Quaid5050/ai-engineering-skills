# Backend deploy strategies

## Order of operations

1. **Additive migrations first** (expand): new nullable columns/tables, new indexes built concurrently. The old code keeps working against the new schema.
2. **Deploy the new code**, which writes both old and new shapes if a migration is in flight.
3. **Backfill** as a job in batches, not inside the migration.
4. **Contract later**: a separate deploy drops old columns or makes new ones required, after no running code or supported client reads the old shape.

A migration that is not additive never runs before the code that needs it; it waits for its own contract deploy.

## Strategies

| Strategy | How | Good for | Watch out |
|---|---|---|---|
| Rolling | Replace instances a few at a time | Stateless services | Old and new code run together: both must accept the schema and the contract |
| Blue/green | Bring up the new version beside the old, switch traffic at once | Fast rollback (switch back) | Database is shared: migrations must suit both colours |
| Canary | Send a small share of traffic to the new version, compare signals, then widen | Risky changes | Needs per-version metrics; sticky sessions may hide problems |
| Feature flag | Deploy dark, switch on per cohort | Behaviour changes, safety-critical paths | Each flag needs an owner and a removal condition |

## Scheduled jobs and workers during a deploy

- **Coordinate scheduling.** Verify the actual runner's clustered/leader/deduplicated-trigger model across old and new instances. Recoverable claims and downstream idempotency still protect effects when triggers or workers overlap; leadership alone is not a delivery guarantee.
- **Drain workers.** On shutdown a worker stops taking new jobs and finishes (or releases) the current one within a grace period; jobs that are re-delivered after a visibility timeout or a late acknowledgement must be idempotent (a stable operation key with recoverable outbox state, `add-scheduled-job` in the backend plugin).
- **Payload compatibility.** A job enqueued by the old version may be run by the new one and the reverse: job payloads change additively, like the API.
- **Pausing:** know how to pause the scheduler and disable one job without a deploy (a flag or an admin command) — it is the first move in an incident with duplicate sends.

## Smoke after deploy

- The readiness/health endpoint (database, migrations applied, caches reachable).
- One authenticated call through the real path.
- Error rate and p95 latency per route compared with before the deploy (`observe`).

## Rollback

- Redeploy the previous image/artifact (keep at least the last good one available).
- Prefer rolling migrations **forward** (a new migration that fixes the problem) over running a down migration, unless the down path was tested on a copy of production-shaped data.
- Feature flag off is the fastest rollback for behaviour changes.
