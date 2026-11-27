---
name: postmortem
description: "Write a blameless postmortem after an incident or any bug where a critical alert was missed or data was exposed — summary, impact, UTC timeline, root cause by five whys, detection (which rung of the testing-doctrine ladder caught it and which should have), what went well, badly and lucky, and follow-ups that prevent, detect earlier or mitigate, each with an issue — then update the skills that would have caught it. Use after SEV1/SEV2 incidents and serious escapes. Trigger on /postmortem, 'write the postmortem', 'incident review', 'what did we learn', 'retro on the outage', 'root cause analysis document'."
argument-hint: "[incident slug, issue or description]"
license: MIT
metadata:
  version: "2.0.0"
---

# Postmortem

Write the postmortem for `$ARGUMENTS` (an incident slug, issue, or description) at `docs/postmortems/<YYYY-MM-DD>-<slug>.md` (or the project's place). Required after SEV1/SEV2 and data-integrity incidents (`incident`), and after any bug where a critical action was missed, records were lost or duplicated, or personal data was exposed. Optional for SEV3 — recommended when a safety-critical path was involved.

**Blameless:** describe what systems, tests and processes allowed it; never who "should have" done something.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

The incident timeline draft, the investigation report, the PRs and releases involved (`gh pr view`, `git log`), signals and links from `observe`, user reports (no personal data), and the project's postmortem location and template if it has one.

## 1. Draft

```markdown
# <Title> — postmortem
Severity: SEV1 | SEV2 | SEV3 · Tracking issue: <link> · Date: · Duration: start–end UTC · Status: draft | final

## Summary
Three sentences: what happened, who was affected, how it was fixed.

## Impact
People affected (counts, platforms, versions), what they experienced, safety impact, data damage and its repair.

## Timeline (UTC)
| Time | Event |
|---|---|

## Root cause
Five whys down to the deepest cause in our control, with evidence links.

## Detection
How we found out. Which rung caught it and which rung **should** have — the ladder is defined once in `testing-doctrine` (quality plugin): type/compile → lint → architecture test → unit/integration test → CI → design review → code review → device test → alert/monitoring → user report.

## What went well / what went badly / where we got lucky

## Follow-ups
| Action | Type (prevent / detect / mitigate) | Issue | Owner | Due |
|---|---|---|---|---|
```

**Gate:** every claim in Root cause and Detection links to evidence; every follow-up has a type.

## 2. Follow-ups

- Each action moves detection **earlier** or makes the class of bug **impossible** (a type, a test, a lint rule, an architecture test, an alert, a device-test row) — never only "be more careful".
- File each through `file-bug` or `file-feature` with the user's OK, and link the issue in the table.
- **Encode the lesson** through `capture-lesson` (meta plugin): the review dimension, the test rule, the placement row, the device-test row. A lesson that stays in this document only will be learned again.
  - **In a project that installed these skills as plugins:** never edit the installed plugin files. Encode it in the project itself — `AGENTS.md`, its conventions, its architecture tests, its own skills (e.g. `.claude/skills/`) — and, with the user's OK, draft an issue for the upstream skills marketplace describing the generalised lesson.
  - **In the marketplace repository itself:** edit the skills, version and changelog as `capture-lesson` describes.

## 3. Finish

Share the draft with the user; mark it `final` after they agree. Commit it on a `docs/<tracking-issue>-<slug>` branch together with the project's own rule and test updates, through a PR that closes the follow-up issues it resolves.

## Rules

- No names attached to mistakes; describe the system.
- No personal data, tokens or precise locations in the document.
- "Root cause unknown" is allowed; then the first follow-up is the investigation that finds it.

## Composition

| From | This skill | To |
|---|---|---|
| `incident`, `bugfix` of a serious escape | The document + follow-up issues | `capture-lesson` (meta), `file-bug`, `file-feature` |
