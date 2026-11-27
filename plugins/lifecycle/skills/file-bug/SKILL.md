---
name: file-bug
description: "Record a bug as an issue with a fixed template — symptom-style title, observed vs expected (citing the spec or design), steps to reproduce from a fresh state, environment, frequency, severity mapped to priority (P0 when a safety-critical path can fail silently, data is exposed or lost), safety impact, evidence with personal data stripped, suspected cause labelled as a theory, and the regression test to add — after the owner's approval, linked to its epic. Trigger on /file-bug, 'file a bug', 'log this bug', 'create a bug issue', 'report this as a bug'."
argument-hint: "[description | error link | user report | --parent <epic> …]"
license: MIT
metadata:
  version: "2.0.0"
---

# File bug

Record `$ARGUMENTS` (a description, an error-tracker link, a user report, or `--parent <epic>` plus a description) as an issue. This skill **records**; `investigate-bug` finds the cause; `bugfix` fixes it. If an investigation already ran in this conversation, put its findings in the issue instead of re-investigating. If `$ARGUMENTS` is empty, ask what happened, where, and what should have happened.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

`AGENTS.md`: tracker, labels, milestones, priority definitions, how versions and environments are named, which paths are safety-critical.

## 1. Gather

| Field | How to fill it |
|---|---|
| Title | `fix(<area>): <symptom in user terms>` ≤ 70 chars — `fix(sync): edits made offline disappear after reconnect`. |
| Observed | What happened, with exact error text. |
| Expected | What should happen, citing the spec or design. |
| Steps | Numbered, from a fresh state. "Not yet reproducible" is allowed — say what was tried. |
| Environment | App version/build, platform + OS, device model or browser, server commit or environment. |
| Frequency | Always / x of y tries / once. |
| Severity → priority | **P0:** a safety-critical path can fail silently, personal data is exposed to the wrong person, or data is lost. **P1:** a core flow is broken with no workaround. **P2:** broken with a workaround, or a non-core flow. **P3:** cosmetic. |
| Safety impact | Can a critical action be missed, delayed or duplicated? Can someone see data they should not? Yes → `safety-critical` and/or `privacy`, at least P1. |
| Evidence | Error-tracker link, log lines, screenshots of synthetic data, a failing test name. |
| Suspected cause | Only what the evidence supports, labelled as a theory. `Unknown` is fine. |
| Areas / Blocked | `area:*`; `blocked` + `blocked:<reason>` + a `**Blocked by:**` line if the fix waits on something. |

## 2. Draft and preview

```markdown
**Severity:** P1 · **Safety impact:** none | critical action can be missed | data exposure | data loss · **Found in:** <version> <platform> / <environment>

### Observed
### Expected
### Steps to reproduce
1. ...
### Environment
### Frequency
### Evidence
### Suspected cause
Theory, not fact: ...
### Regression test to add
The test that fails today and passes after the fix: `<path>` — `<name>`.
```

**Privacy check:** strip names, emails, phone numbers, addresses, coordinates, account ids, tokens and session ids from text, logs and screenshots. Refer to people as User A/B.

Show the owner title, labels and body. Create nothing until they approve.

## 3. Create and link

```bash
gh issue create --title "<title>" --body-file <file> --label "type:bug,P1,area:sync,safety-critical" --milestone "<milestone of the feature it breaks>"
```

Attach to the feature's epic when it belongs to one (`file-feature` §3 commands). Found in a merged PR → comment the issue link on that PR only with the owner's OK.

## 4. Report

Issue link, priority, and the next step: `investigate-bug` when the cause is unknown, `bugfix` when an investigation already proved it (bugfix still needs that report; a cause you only suspect goes through `investigate-bug`).

## Rules

- P0 and `safety-critical` bugs go at the top of the reply, not buried.
- Never paste personal data; never attach a real user's screenshot.
- A theory stays labelled as a theory; "not our bug" needs evidence.
- One bug per issue; two symptoms with one proven cause → one issue listing both.

## Composition

| From | This skill | To |
|---|---|---|
| A report, `investigate-bug`, `incident`, a review finding | One bug issue | `investigate-bug` or `bugfix` |
