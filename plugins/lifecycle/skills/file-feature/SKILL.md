---
name: file-feature
description: "File one already-scoped feature slice as an issue with a fixed template — outcome-style conventional title, design frame, MVP id and milestone, priority, areas and flags (safety-critical, privacy, needs-device-test), what and why, 3–7 checkable acceptance criteria including failure states, tests to write first, approach, out of scope, open questions — after a privacy check and the owner's approval; optionally attached to an epic. Trigger on /file-feature, 'file this feature', 'create an issue for', 'open a feature issue', 'track this as an issue'."
argument-hint: "[one-line feature | design frame | --parent <epic> description]"
license: MIT
metadata:
  version: "1.0.0"
---

# File feature

File `$ARGUMENTS` (a one-line feature, a design frame, or `--parent <epic>` plus a description) as an issue. Use it **after** the slice is scoped: you know what the person will be able to do and how to tell it is done. Not scoped yet (fuzzy goal, competing approaches, several risky areas) → `investigate-feature` and `spec` first. If `$ARGUMENTS` is empty, ask for the feature in one line.

## 0. Read the project

`AGENTS.md`: the tracker and repository, the label set, milestone names, priority definitions, where specs live. Missing labels → offer the `bootstrap-project` label script (it changes the repo: owner's OK).

## 1. Gather

Fill every field from the conversation, the spec and the design. Ask at most **one** question, only for what you cannot infer (usually priority). Called by `feature-to-issues`: everything is approved — ask nothing, change nothing.

| Field | How to fill it |
|---|---|
| Title | Conventional, ≤ 70 chars, the user-visible outcome: `feat(bookings): guest gets a confirmation when a slot is booked`. Not the implementation (`add bookings table`). |
| Design | Frame id + title exactly as in the design source. No design → link the spec's approved state table and low-fidelity flow; if those are not approved yet either, add the `needs-design` label (the slice cannot start until they are). |
| MVP item | The feature id and milestone from the MVP scope, or `post-MVP`. |
| Priority | `P0`–`P3` per the project's definitions. |
| Blocked | `blocked` + `blocked:<reason>` labels and a `**Blocked by:**` line. |
| Areas | `area:*` labels for each module touched. |
| Flags | `safety-critical` (on the project's safety-critical list in `AGENTS.md`; otherwise: a silent failure can harm a person, lose money or lose data) · `privacy` (personal data, sharing, consent) · `needs-device-test` (background work, notifications, widgets, battery, hardware). |
| What / Why | 1–2 sentences each; link the spec section. |
| Acceptance criteria | 3–7 checkable bullets in user language, including the failure states the design or spec shows (offline, permission denied, empty, error). |
| Tests to write first | From the criteria, from the caller's point of view (UI test, API integration test, domain unit test). A criterion that cannot become a failing test is not ready — fix the criterion. |
| Approach | One short paragraph: likely folders, existing patterns to copy, skills to use. Not a design doc. |
| Out of scope / Open questions | Explicit. |

## 2. Draft and preview

Use this template exactly; never add or drop a section (write `None`).

```markdown
**Design:** <frame> · **MVP:** <id · milestone> · **Spec:** docs/specs/<NNN>-<slug>/spec.md#<section>

### What
### Why
### Acceptance criteria
- [ ] ...
### Tests to write first
- [ ] `<test path>` — <behaviour>
### Approach
### Out of scope
### Open questions
<details><summary>Context</summary>Links: spec, investigation, related issues, design.</details>
```

**Privacy check** before preview: no real names, addresses, phone numbers, emails, coordinates, account ids or screenshots of real data in title or body. Use "User A / User B" or synthetic ids.

Show the owner the title, labels, milestone, parent and body. **Create nothing until they approve** (approval already in the request — "file it" — counts).

## 3. Create

Write the approved body to a file, then:

```bash
gh issue create --title "<title>" --body-file <file> --label "type:feature,P1,area:server" --milestone "<milestone>"
```

Attach to an epic when `--parent` was given or the spec has one:

```bash
gh api repos/<owner>/<repo>/issues/<child> --jq .id                    # numeric id, not the number
gh api repos/<owner>/<repo>/issues/<epic>/sub_issues -X POST -F sub_issue_id=<id>
```

A child that already has another parent needs `replace_parent=true` and the owner's OK. Other trackers: the equivalent "create + link to parent" calls.

## 4. Report

Issue link, labels, parent, and the first test to write. Add the row to the spec's `issues.md` if there is one.

## Rules

- One issue = one vertical slice a person can use. Never "add the table" / "add the endpoint" / "add the screen" as separate issues.
- Never create, label or link without approval; never edit someone else's issue unasked.
- Feature labels (`feature:<slug>`) are created by `feature-to-issues`.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-feature`, `spec`, `feature-to-issues` (per slice), the conversation | One issue | `start-issue` |
