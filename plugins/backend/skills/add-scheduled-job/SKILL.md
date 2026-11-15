---
name: add-scheduled-job
description: "Add or change server-side scheduled and background work and the outbound notifications it sends — first ask whether a stored 'until' time is enough; otherwise one scheduler instance (never two during a deploy), idempotent jobs that may run twice, rows claimed with a lease or skip-locked, a unique sent-ledger keyed by thing + due time, access re-checked at run time, zone-aware schedules with DST tests, notifications through one port with templates and preferences/unsubscribe, one retry owner, metrics and alerts for lag and failures, failure-path tests first. Use for reminders, digests, expiries, escalations, retries and cleanup jobs. Trigger on /add-scheduled-job, 'cron job', 'scheduled task', 'send a reminder', 'background job', 'send an email when', 'notification sent twice', 'job queue', 'worker'."
argument-hint: "[what must happen, and when]"
license: MIT
metadata:
  version: "1.0.0"
---

# Add a scheduled job

Add or change the server-side job for `$ARGUMENTS` (what must happen, and when). If empty, ask: what must happen, at what time or after what event, to whom, and what is the harm if it happens twice or never.

Scheduled work fails in two quiet ways: it **never runs** (nobody notices) or it **runs twice** (a person gets two reminders, or two charges). Both are designed out here, and both get tests. Jobs that send something people rely on are **safety-critical** when the project's list in `AGENTS.md` says so.

## 0. Read the project

1. `AGENTS.md`, the conventions and placement table (`engineering-principles` §3, lifecycle plugin), decision records: is there a job runner, a scheduler, an outbox, a notification port already? Reuse it.
2. The stack's job tooling and its delivery semantics (at-least-once? visibility timeout? one scheduler?) — see the stack references of `backend-conventions` (this plugin) and [references/stacks.md](references/stacks.md).
3. How the app is deployed (rolling, blue/green, several replicas) — it decides how "exactly one scheduler" is guaranteed.

**Gate:** you can name the runner, the scheduler, where jobs live, and what happens to an in-flight job when a deploy starts.

## 1. Do you need a job?

- A **state that changes with time** ("suspended until 17:30", "trial ends on …") is a stored timestamp the reads compare with `now` — no job.
- A job is needed only when something must **happen** at a time: send, charge, escalate, expire with side effects, clean up.

## 2. Design

| Decision | Rule |
|---|---|
| Who schedules | **One scheduler instance** per environment, guaranteed (a lock, a single replica, the platform's cron) — including during deploys, when old and new versions overlap. Workers may be many; the scheduler is one |
| What the job does | Thin: load ids, call **one** use-case method (`backend-conventions` §2). Rules live in the domain, not in the job |
| Finding work | Query due rows in bounded batches and **claim** them (row lock with skip-locked, or a lease column with an expiry), so two workers never take the same row |
| Exactly-once *effect* | Delivery is at-least-once, so the effect is made once: a **sent-ledger** row with a unique key (`thing id + due time`, or `thing id + kind`) inserted **before** sending; a unique violation means "already sent" → skip. The ledger also records the result |
| Access at run time | Re-check membership, consent and preferences **when the job runs**, not only when it was scheduled — a removed member or a cancelled order gets nothing |
| Time | Schedules in the person's **zone** (store the IANA zone id + local time); compute the instant in the domain; DST gaps and overlaps decided explicitly and tested |
| Retries | **One retry owner**: the job (bounded attempts, backoff with jitter, then a visible failure: a dead-letter row, an alert, a fallback channel). The sending client does not retry on its own |
| Enqueue after commit | A job triggered by a change is enqueued **after** the transaction commits (or through an outbox row in the same transaction) — never before |
| Deploys | Workers drain gracefully (finish or release their claim); a lease expiry returns abandoned rows; schema changes stay compatible with jobs already queued |
| Observability | Metrics: job lag (due → done), failures by kind, ledger "already sent" count, backlog size; an alert with an owner for each safety signal (`observe`, lifecycle plugin) |

### Outbound notifications (email, SMS, push, webhooks)

- **One notification port** with one adapter per provider; features never call a provider SDK directly.
- **Templates in one place**, keyed by notification kind and language; no message text assembled in jobs.
- **Preferences and unsubscribe** checked at send time; transactional vs marketing kinds kept apart; every non-essential message has an unsubscribe path.
- No personal data in logs, metrics or the ledger beyond ids (`security-privacy-review` §5, quality plugin).
- Provider failures: timeout + circuit breaker on the client, retries only by the job; a fallback channel for critical messages if the spec requires one.

**Gate:** the design names the scheduler guarantee, the claim mechanism, the ledger's unique key, the retry owner and the re-check — reviewed in `design-review` (lifecycle plugin).

## 3. Tests first (failure paths first)

With an injected clock and a recording fake of the notification port (`testing-doctrine`, quality plugin):

- the job runs **twice** for the same due item → **one** notification, one ledger row — **paired with** a test that a genuinely new due item (the next occurrence, a second chore) still sends;
- two workers claim concurrently → each item handled once (a race test with a gate, never a sleep);
- the member was removed / unsubscribed / the item cancelled before run time → nothing sent, ledger records why;
- provider error → retried with the exact backoff sequence, then a visible failure (dead letter + metric);
- the process dies after sending, before recording → the next run does not send again (the ledger was written first) **or** the design states and tests the accepted risk;
- exactly at the due instant (not one tick early, not never); DST spring-forward and fall-back for a local-time schedule; a far time zone;
- enqueue after commit: a rolled-back change enqueues nothing.

**Gate:** every test is red first for the right reason.

## 4. Build and verify

Build per `backend-conventions`; schema for the ledger and lease columns via `add-migration` (this plugin) with the unique index. Verify locally with the real database and the real runner (one scheduler, two workers), then run the area suite. The PR states the scheduler guarantee during deploys, the failure modes and how each is tested; `deploy-check` (lifecycle plugin) covers the deploy overlap.

## Rules

- Never two schedulers; never a job without idempotency; never send before the ledger row exists.
- Never swallow a job failure: it is retried by its owner or becomes a visible failure.
- Never decide *whether* to notify in an adapter; the use case decides.
- Changing timing or frequency of something people rely on goes through `spec` (lifecycle plugin) first.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `spec`, `design-review` (lifecycle), `backend-conventions` | Scheduler, claim, ledger, notifications, tests | `add-migration`, `add-endpoint` (this plugin); `observe`, `deploy-check` (lifecycle); `security-privacy-review` (quality) |
