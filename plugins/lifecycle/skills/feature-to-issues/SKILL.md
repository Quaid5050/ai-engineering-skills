---
name: feature-to-issues
description: "Break an approved spec into an epic with sub-issues — vertical slices a person can use end to end, ordered riskiest first (safety and technical risk, then dependency, then learning, then the rest), spikes for research, every must requirement and every safety failure mode owned by a slice, priorities from must/should/could — shown in full for approval before anything is created, then created and linked, and a manifest saved. Trigger on /feature-to-issues, 'break this into issues', 'create the issues for this feature', 'make an epic', 'create sub-issues', 'slice this spec'."
argument-hint: "[spec path, NNN or slug]"
license: MIT
metadata:
  version: "2.0.0"
---

# Feature to issues

Turn the approved spec for `$ARGUMENTS` (a spec path, `NNN` or slug) into one epic plus one sub-issue per vertical slice, then open the docs PR. No approved spec → run `spec` first. A single-slice feature skips the epic: `file-feature`.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

- `AGENTS.md`: the tracker, label set, milestones, priority definitions.
- `docs/specs/<NNN>-<slug>/spec.md` — must say `status: approved`, else stop and ask. Read `investigation.md` too: rejected approaches must not come back as issue solutions.
- Existing issues, so nothing is filed twice:
  ```bash
  gh issue list --search "<slug> in:title,body" --state all
  ```

## 1. Slice

**Vertical slices only.** Each issue, when merged, gives a person something usable end to end (screen → API → data → platform where needed).

| Bad (layers) | Good (slices, riskiest first) |
|---|---|
| Add `bookings` table · Add bookings API · Add bookings screen | 1. A guest books a free slot and gets a confirmation, on the slowest path (thinnest path through the riskiest part) · 2. The booking survives a lost connection mid-submit (no double booking) · 3. The host sees and cancels bookings · 4. Reminders · 5. Edit and reschedule |

The first slice may be plain, but usable end to end; it retires the biggest risk early. Research needed before any slice can be designed is a **spike** (`type:chore` + `spike`, time-boxed; its output is a decision written into the spec, not merged code).

**Order:** (1) safety and technical risk — what we are least sure works; (2) dependency risk — schema, contract; (3) learning risk — the slice that tests an assumption; (4) the remaining happy paths, edges, polish.

Each slice names the requirements it covers. Every **must** appears in some slice; every safety failure mode in the spec is someone's acceptance criterion.

**Gate:** coverage check — list each must requirement and each failure mode with the slice that owns it; no gaps.

## 2. Present for approval

```
## Issue breakdown: <Feature>  (spec: docs/specs/NNN-slug/spec.md)
Ordering: <one sentence why>

| # | Title | Covers | P | Risk retired | Areas | Flags |
|---|---|---|---|---|---|---|
| 1 | feat(bookings): guest books a free slot and gets a confirmation | R1, R4 | P1 | double booking under retry | server, client | safety-critical |

Epic: "<Feature>" — <n> sub-issues
```

Priority: a slice with any **must** → `P1`; only **should** → `P2`; only **could** → `P3`. `P0` is for urgent bugs and incidents, never planned work. The epic takes the highest priority of its slices.

Below the table show **every issue body in full** (the `file-feature` template, privacy check run on each). The owner approves table and bodies together; nothing is created from a table alone. **Wait for approval**; adjust and re-present when asked.

## 3. Create

1. Make sure the label set exists (`bootstrap-project` labels; with the owner's OK the first time); create `feature:<slug>`.
2. **The epic** — created **here** (it may already exist if `spec` created it to post the spec-level design review; then update it, never create a second one). Title = feature name, `type:epic`, `feature:<slug>`, the highest slice priority, the milestone. Body: spec link, 2–3 sentences of problem, the ordered slice list (numbers filled after step 3). Attach the docs issue from `investigate-feature` to it as a sub-issue.
3. **Each slice** through `file-feature --parent <epic>` with the approved title, body and labels, in order so numbers follow the slice order. The approval covers these: `file-feature` must not ask again or change the bodies. An existing issue that belongs here is linked, not re-created.
4. Confirm the sub-issues are attached:
   ```bash
   gh api repos/<owner>/<repo>/issues/<epic>/sub_issues --jq '.[] | "\(.number) \(.title)"'
   ```
5. Write `epic: <number>` into the spec front matter; save `docs/specs/<NNN>-<slug>/issues.md` (the table with real numbers and links); commit on the docs branch (`docs/<docs-issue>-<slug>`).
6. **Now open the docs PR** with `create-pr` (investigation + spec + `issues.md`; `Closes #<docs issue>`). If a docs PR is already open, push to it instead. Slices start only after it is merged.

## 4. Report

Epic link, sub-issue count by priority, the docs PR link, and the first issue to start once the docs PR is merged (`start-issue`).

## Rules

- Never create issues without approval; never re-create one that exists.
- As small as possible but complete: prefer more, thinner slices.
- Each slice's "Tests to write first" must be writable from its acceptance criteria alone.
- Bugs found during the feature go through `file-bug --parent <epic>`.

## Composition

| From | This skill | To |
|---|---|---|
| `spec` (approved) | Epic + ordered sub-issues + `issues.md` + the docs PR | `file-feature` (per slice), `create-pr` (docs), then `start-issue` on slice 1 |
