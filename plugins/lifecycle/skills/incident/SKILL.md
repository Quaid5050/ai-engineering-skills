---
name: incident
description: "Handle a live production problem — declare severity in the first minutes (SEV1 when people may be unsafe or data is exposed or leaked, SEV2 when a core flow is broken, SEV3 when degraded), stop the harm first (halt the rollout, roll back, switch a flag off, cut a leaking endpoint), keep a timeline, draft communication for the user's OK, investigate read-only, fix through the normal bugfix path, verify recovery with the same signal that showed the problem, and hand off to a postmortem. Use when something is broken for real users. Trigger on /incident, 'prod is down', 'users can see other users data', 'payments failing', 'notifications not arriving', 'emergency', 'everything is broken', 'outage'."
argument-hint: "[what is happening]"
license: MIT
metadata:
  version: "2.0.0"
---

# Incident

Handle the live problem in `$ARGUMENTS`. Speed matters, but production actions require explicit scope or an existing incident/runbook authorization; reuse valid approval rather than repeatedly interrupting containment.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

From `AGENTS.md` and runbooks (`docs/runbooks/`): how to halt a rollout, roll back each release path, switch feature flags, reach the status page or in-app messaging, and which dashboards show the safety signals. Missing runbook → note it as a postmortem follow-up; do not improvise destructive steps.

## 1. Severity (decide in the first minutes)

| SEV | Means | Examples |
|---|---|---|
| **SEV1** | People may be unsafe, or data is exposed or leaked | Critical alerts or messages not delivered; one user sees another's private data; data loss; mass crash on launch |
| **SEV2** | Core flow broken, safety intact | Sign-in failing; checkout failing for many; background sync stale for many users |
| **SEV2 (data integrity)** | Records duplicated, corrupted or lost — **SEV1** when it touches safety, money, or exposes data at scale | A submission stored twice; reminders sent twice; edits lost after sync |
| **SEV3** | Degraded, a workaround exists | One screen broken, one device maker affected, slow reports |

When unsure, pick the higher one. The project's safety-critical list in `AGENTS.md` decides what counts as "safety".

**Severity ↔ issue priority:** SEV1 ↔ P0 · SEV2 ↔ P0 or P1 · SEV3 ↔ P2.

**Track the incident without delaying containment:** open an issue when tracking is authorized, or keep a local timeline until it is: title `incident: <symptom>`, the severity's priority, `safety-critical`/`privacy` labels as they apply. The timeline, the fix and the postmortem all link to it.

## 2. Stop the harm first (mitigate before root cause)

Options, fastest first — check existing authorization, obtain approval only for new scope, act, verify:

1. Halt the staged store rollout.
2. Roll back the over-the-air patch or the backend deploy to the last good version (`release` rollback).
3. Switch off the feature flag for the broken behaviour.
4. **Privacy leak:** cut the leaking endpoint or method (return not-found) even if a feature breaks.
5. **Critical delivery failing:** confirm the fallback channel works; if it does not, that is the first fix.
6. **Duplicate or runaway scheduled effects** (messages sent twice, repeated charges): **pause the scheduler or disable the one job**, stop or drain the worker queue, and only then investigate; check for two scheduler instances (a deploy that left both running).

**Gate:** the harm has stopped (the signal that showed it is back to normal) or the user has decided to accept it while the fix is made.

## 3. Keep a timeline

From the start, in a draft at `docs/postmortems/<YYYY-MM-DD>-<slug>.md` (or the project's place): time (UTC) — what was seen — what was done — by whom. Facts only.

## 4. Communicate

Draft — do not send without the user's OK — a status or in-app message for affected users when safety or data is involved ("Notifications may be delayed; contact people directly if it is urgent"), and an update every 30–60 minutes until resolved. Say what is known and when the next update comes; never guess.

## 5. Investigate

`observe` for the window, then `investigate-bug` for the cause. Read-only queries only (`data-check`, backend plugin). Keep facts and hypotheses apart.

## 6. Fix and verify recovery

The fix goes through `bugfix` (regression test, `create-pr`, `ci`, `merge`); the release path from `release`. Recovery is verified with **the same signal that showed the problem** (delivery and uncertain-outcome backlog back within the defined recovery targets, crash-free back above target), not with "the deploy finished". Stored data damage (wrong records, missing history, wrong messages sent) is listed and its repair planned separately.

## 7. Close

Severity, start/end times, impact (how many users, what they experienced), mitigation, root cause (or "unknown yet"), follow-up issues. Then `postmortem` — **required for SEV1, SEV2 and any data-integrity incident**, optional (recommended) for SEV3.

## Containment and recovery

Authorized urgent reversible containment can precede ordinary issue/review ceremony. Assign incident command, technical and communication owners; preserve restricted forensic evidence. For credential compromise or corruption, plan revocation/repair and restoration, not merely application rollback. Verify recovery with expected/control data and user-visible health; follow up with an effectiveness check. Use `recovery-drill` (operations plugin) when available.

## Rules

- Mitigate first, investigate second.
- Never delete data, rewrite history or change production data during an incident without an explicit, specific OK.
- Never message users or post publicly without the user's OK.
- No guessing in updates.

## Composition

| From | This skill | To |
|---|---|---|
| `observe`, a user report, an alert | Mitigation, timeline, recovery | `investigate-bug`, `bugfix`, `release` (rollback), `postmortem` |
