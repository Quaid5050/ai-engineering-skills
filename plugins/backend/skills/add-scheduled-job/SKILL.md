---
name: add-scheduled-job
description: "Add or change server-side scheduled and background work and the notifications it sends — first ask whether a stored 'until' time is enough; otherwise persist intent in a durable outbox with the business change, claim work with recoverable leases, scope idempotency to the operation, model uncertain outcomes explicitly, re-check access and consent at run time, zone-aware schedules with DST tests, notifications through one port with templates and preferences, one retry owner, metrics for lag and failures, crash-window tests first. Use for reminders, digests, expiries, escalations, retries and cleanup jobs. Trigger on /add-scheduled-job, 'cron job', 'scheduled task', 'scheduled job', 'send a reminder', 'background job', 'background worker', 'send an email when', 'notification sent twice', 'duplicate notification', 'missed delivery', 'retry a failed send', 'job queue', 'worker'."
argument-hint: "[what must happen, and when]"
license: MIT
metadata:
  version: "2.0.0"
---

# Add a scheduled job

Design the work in `$ARGUMENTS`. Establish what must happen, the deadline and the harm of loss or duplication. Do not promise exactly-once effects without an end-to-end protocol that actually provides them.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

Find the runner, schedule store, transaction boundaries, deployment topology, existing outbox and provider contract. Read only the relevant [stack reference](references/stacks.md). Determine provider idempotency scope/expiry and whether an acknowledgement means accepted, processed or delivered.

## 1. Choose the execution model

A time-dependent read can often compare a stored timestamp without a job. Use work scheduling for actual side effects. Use a single leader only if the chosen scheduler requires it; clustered schedulers and duplicate triggers are acceptable when dispatch is coordinated and processing remains idempotent. A scheduler lock alone does not deduplicate downstream effects.

## 2. Persist intent and model outcomes

1. Commit business state and a unique pending outbox item in the same transaction. An after-commit callback may wake a dispatcher, but must not be the only record of required work.
2. Scope the operation identity to tenant, subject, kind and occurrence. A duplicate key means the operation exists: inspect its state; it does not prove delivery. Reject reuse with a different payload.
3. Claim pending work using an atomic conditional update or a short transaction, with an expiring lease and ownership token. Do not hold a database lock while calling a provider. A stale worker cannot acknowledge or overwrite a newer claim.
4. Recheck authorization, cancellation and consent before sending. Record a permitted cancellation distinctly from successful delivery. Do not log sensitive payloads; identifiers may also be sensitive.
5. Send with the same stable provider idempotency key on retries when supported. Only record the completion level actually confirmed by the provider.
6. Recover expired claims. A timeout or crash after sending can leave the outcome unknown: reconcile with the provider or retry with its idempotency guarantee. Without either, explicitly choose between duplicate risk and loss risk; escalate uncertain high-impact operations instead of inventing certainty.

States distinguish pending, leased, acknowledged, retryable, uncertain, cancelled and permanently failed. Record attempt count, next eligible time, ownership token and safe error category. Retain deduplication records for the supported replay horizon; document behavior after expiry or deletion.

**Gate:** the design defines durable intent, each transition, crash recovery, provider guarantees, reconciliation and the allowed duplicate/loss policy.

## 3. Bound retries and deployment behavior

One layer owns the attempt budget and backoff. Honor server delays and deadlines; coordinate rather than multiply provider, queue and worker retries. Exponential backoff with jitter, timeouts, concurrency limits and a visible terminal/recovery path prevent retry storms.

Compute recurring schedules from local time plus a stored zone and an explicit gap/overlap policy. Graceful shutdown stops claims and completes or releases work; expiry also recovers abrupt termination. Old queued payloads and overlapping worker versions must remain compatible. Outbound notifications (email, SMS, push, webhooks) go through one notification port; read [references/notification-port.md](references/notification-port.md) when the job sends anything to a person or another system.

## 4. Verify failure paths

Use a controllable clock, a provider test double with explicit acknowledgement/idempotency semantics and real storage integration tests:

- crash before/after the business transaction: committed work remains pending; rolled-back work does not send;
- crash after claim but before send: lease expiry enables recovery;
- provider accepts then acknowledgement is lost: stable-key reconciliation/retry, or explicit uncertain state without a fabricated guarantee;
- crash after acknowledgement but before local completion: replay does not silently lose the operation;
- two workers and an expired lease: stale completion cannot overwrite the current owner; receiver deduplication still handles overlapping sends;
- genuine second occurrence sends; duplicate operation identity does not create a second logical operation;
- removed access, consent withdrawal, permanent rejection, bounded retries and operator recovery;
- zone transitions, overdue catch-up and deploy overlap.

New regression tests must fail for the intended defect; characterization tests may start green with a justified fault/mutation check. Verify with the actual runner and storage before release.

## 5. Report

State guarantees and residual risks, transition/lease design, tested crash windows, supported replay horizon, backlog age, uncertain outcomes, retry exhaustion and alert/runbook ownership. Measure the agreed delivery SLO; do not equate provider acceptance with delivery to a person.

## Rules

- Persist required intent before dispatch; never treat a unique conflict as evidence of completion.
- Never lose pending work silently or report unknown as successful.
- Scheduling coordination, local ownership fencing and receiver idempotency solve different problems; document each required mechanism.
- Use `deploy-check` and `security-privacy-review` for relevant release and access changes.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `spec`, `backend-conventions` | Durable job and recovery contract | `add-migration`, `add-endpoint`, `observe`, `deploy-check` |
