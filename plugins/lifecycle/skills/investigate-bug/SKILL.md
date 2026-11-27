---
name: investigate-bug
description: "Find the root cause of a bug — reproduce it first with a failing test or on a device (on a fix branch linked to the bug issue), pin the symptom, keep evidence-backed competing hypotheses with facts and theories apart, narrow with code history, logs, error tracker and read-only data, drive to the deepest cause in our control with causal analysis, measure the blast radius, and write the report including how to prevent the whole class. Trigger on /investigate-bug, 'why is this happening', 'root cause this', 'dig into this bug', 'figure out what is wrong', 'this stopped working', 'debug this'."
argument-hint: "[symptom, issue number, error link, or user report]"
license: MIT
metadata:
  version: "2.0.0"
---

# Investigate bug

Find the root cause of `$ARGUMENTS` (a symptom, an issue, an error-tracker link, or a user report). This skill diagnoses; `bugfix` fixes. If empty, ask: what happened, where (device, OS, version, environment), what was expected, how often.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

`AGENTS.md`: how to run tests and the app locally, where logs and errors go, which paths are safety-critical, read-only access to data (`data-check`, backend plugin). An issue number → read it first (`gh issue view <n>`).

**Safety-critical symptom** — on the project's safety-critical list in `AGENTS.md` (that list wins over the examples here), or by default a critical action missed or duplicated, data exposed to the wrong person, data lost or corrupted → tell the owner **immediately**, before the full investigation. A live production problem → `incident` first.

## 1. Reproduce first

Use the existing task or issue as context. Create an issue only when project policy or coordination needs it; direct authorized fixes may use a descriptive branch without an issue number. Reuse a reproduction already supplied. A reproduction test may precede implementation review. Keep production/shared data read-only.

| Kind of bug | How to reproduce |
|---|---|
| Domain / server logic | One unit test with the same inputs; a fake clock for anything time-based |
| API / auth / data | An integration test through the real entry point against a real local database |
| UI / client state | A UI test; fake time for timers; in-memory fakes at the boundaries for data |
| Background / platform | Emulator or simulator steps from `device-test` (mobile plugin); capture the device logs |
| Device- or vendor-specific | The `device-test` steps on the named device; note its battery and permission settings |

Run it and confirm it fails (**RED**) for the reported reason. A failing setup is not a reproduction. Cannot reproduce yet → reproducing **is** the goal; record each attempt.

## 2. Pin the symptom

What exactly is observed; when (always, after an action, only in the background, only on one vendor's devices); since when (`git log --since`, the release); what was expected (spec or design).

## 3. Hypotheses

Write plausible competing explanations; do not invent a minimum number. Start with the smallest experiment that distinguishes them. Typical: a permission downgraded by the OS, background work killed, a stale cache, a timezone or UTC conversion, duplicate or out-of-order events, a wrong tenancy/membership filter, an expired token, an offline queue not flushed, a race between two channels (push vs pull), a retry layer doubling a send.

```
FACTS (with source)                 THEORIES (unconfirmed)
H1: … → evidence … → confirmed | rejected because …
```

Record why each is rejected — it stops the next person repeating it. After three rejections, re-check your assumptions instead of trying variations.

## 4. Narrow with evidence

- **Code:** trace from the symptom back to the entry point; `git log -L` / `git log --oneline -20 -- <file>`; read every `catch` on the path.
- **Errors and logs:** the error tracker (release, breadcrumbs), server logs, `observe` for error rate and latency in the window.
- **Data:** read-only queries (`data-check`) comparing what the code produced with what it should have; aggregate or redact, never paste personal data.
- **Device:** device logs, battery and permission state.

## 5. Causal explanation

Trace causal contributors only as far as evidence supports; use a graph when failures interact, and label unresolved causes. Fix target = the deepest cause in our control, **plus** "why was this breakable?" (a missing test, type, lint rule, alert or placement row) — name the rung on the ladder in `testing-doctrine` (quality plugin) where it should have been caught.

## 6. Blast radius

Who else is affected: other platforms, vendors, versions, tenants; other code with the same pattern (`grep`); stored rows that are wrong and need a repair after the fix.

**Gate:** a reproduction that fails for the reported reason and a cause chain backed by facts — otherwise the status is "unverified".

## 7. Report

For substantial investigations save `docs/investigations/<YYYY-MM-DD>-<slug>.md`; for a scoped fix keep the evidence in the task or PR:

```markdown
# <symptom>
Issue: <link> · Status: root cause found | not reproduced | unverified

## Reproduction        (test name or exact steps; RED output)
## Root cause          (supported causes, uncertainty, file:line)
## Evidence            (facts with sources)
## Ruled out           (hypothesis → why rejected)
## Blast radius
## Proposed fix        (approach, not code) and the regression test
## Prevent the class   (type, lint, test, alert or placement row that would have caught it earlier)
```

## 8. Next step

If tracking is needed, use `file-bug` with this report. Fix wanted → `bugfix` (it reuses the report and the failing test).

## Rules

- No reproduction, no confident root cause: say "unverified" and name the missing evidence.
- Facts and theories never blur; label every claim.
- Read-only for production and shared data: no writes, no data fixes, no code fixes. The only code added is the reproduction test, on the fix branch.

## Composition

| From | This skill | To |
|---|---|---|
| A report, `file-bug`, `incident` | Report + failing reproduction test | `file-bug`, `bugfix`; `capture-lesson` (meta) for "prevent the class" |
