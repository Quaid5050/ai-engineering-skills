---
name: spec
description: "Write and get approval for a feature spec — problem and users, designs and states, numbered must/should/could requirements with checkable acceptance criteria, API contract with who may call what, data and migration risk, client and platform/background behaviour, safety failure modes and privacy rules each becoming criteria, analytics, performance budgets, rollout and rollback, risks and open questions — reviewed by a fresh agent and always design-reviewed by the architect agent before approval. Use for anything multi-area, schema-changing, safety-critical or privacy-relevant. Trigger on /spec, 'write a spec', 'spec this feature', 'PRD', 'technical design for', 'plan this feature'."
argument-hint: "[feature name, MVP id, or spec folder]"
license: MIT
metadata:
  version: "1.0.0"
---

# Spec

Write the spec for `$ARGUMENTS` at `docs/specs/<NNN>-<slug>/spec.md` — the same folder and docs branch (`docs/<docs-issue>-<slug>`) `investigate-feature` created. If `$ARGUMENTS` is empty, ask which feature. A small, clear change goes straight to `file-feature`.

## 0. Read the project

- `AGENTS.md`: where specs live, the contract file, the commands, the tracker.
- The investigation `docs/specs/<NNN>-<slug>/investigation.md`. Missing → run `investigate-feature` first; never write a spec from memory of the product.
- The conventions and placement table (`engineering-principles`; the stack conventions skills) — the spec names real files and patterns.

**Gate:** you have the design read, the brief section, the code this touches, and the open questions.

## 1. Draft

Keep every heading; write `None` when empty.

```markdown
---
status: draft          # draft → approved (owner said so) → in-progress → shipped
epic:                  # filled by feature-to-issues
mvp: B2
design: [<frame ids>]
---
# <Feature>

## Problem and users
## Design and states
Each frame: what it shows, which states (loading, ready, empty, error, offline, permission denied, stale).
No design yet → the state table (screen × state → what the person sees and can do) and the low-fidelity flow from the investigation; the owner approves them with the spec.
## Requirements and acceptance criteria
R1 … Rn, each **must / should / could**, each with checkable criteria in user language.
## API contract
Method, path, request, response, errors (stable codes), auth, who may call it (and the forbidden callers).
## Data
Entities, tables, constraints, indexes, retention, migration risk on large tables (expand → migrate → contract).
## Client (web / mobile)
Screens and their states, where the code lands per the client's conventions, routes, offline behaviour, strings.
## Server jobs and scheduling
Scheduled or background server work and outbound notifications (`add-scheduled-job`, backend plugin): trigger, idempotency key, what is re-checked at run time, time zones, what happens on a deploy. `None` if there is none.
## Platform and background work (mobile)
Background tasks, permissions, widgets, push; expected battery cost and how it is measured.
## Files and uploads
Attachments, size caps, metadata stripping, when the parent record is complete (`add-file-upload`, backend plugin). `None` if there are none.
## Safety failure modes
For every critical action: no network, app killed, permission revoked, server down, duplicate and late events. Each maps to a test.
## Privacy and abuse
What is shared with whom, consent, visibility to the person concerned, retention, what is never logged or sent to third parties; how it could be misused against someone.
## Analytics
Events (names, allowed properties) — `analytics-event` (quality plugin).
## Performance budgets
## Rollout and rollback
Flag or not, release path, migration/backfill order, how to turn it off.
## Risks and open questions
Ranked risks with how each is retired (spike, test, device test). Open product questions, each with an owner.
## Out of scope
```

Rules for the draft:
- Requirements describe behaviour a person sees, not code.
- Every safety failure mode and every privacy rule becomes at least one acceptance criterion.
- Name the existing files and patterns to follow; a new pattern needs a decision record (`decision`, meta plugin).
- Open questions stay open; recommend, don't decide for the owner.

## 2. Review (fresh eyes)

Spawn a fresh agent (no access to this conversation) with only the spec path and `AGENTS.md`. Ask it to find: untestable requirements, missing failure modes on critical paths, privacy gaps, unstated battery or cost, API calls without an authorisation rule, contradictions with the design. Fix what holds up; list what you rejected and why under `## Review notes`.

## 3. Design review

Run `design-review` on the technical part — **always** by the `architect` agent (agents plugin), whatever the spec's size — and fold its decisions, reuse and risks into the spec. Post it on the **epic** when the feature will have several slices (create the epic first with `feature-to-issues` step 3.2 if it does not exist yet), otherwise (a single-slice feature, whose issue does not exist yet) on the **docs issue** from `investigate-feature`. Each slice still gets its own short slice-level review before its first production-code commit (`start-issue`). A design finding the spec does not resolve blocks approval.

**Gate:** the review notes and the design review are in the spec; no open design finding.

## 4. Approval

Show the owner: requirements, top three risks, open questions (and the state table and flow when there is no design). Set `status: approved` only after they say so and commit (`docs(specs): <feature> spec`). Then:
- multi-slice → `feature-to-issues`, which adds `issues.md` to the same branch; **then** open the docs PR with `create-pr` (it closes the docs issue, not the epic);
- one slice → `file-feature`, then open the docs PR.

Slices start only after the docs PR is merged (or they pin the spec commit they were planned against).

## Rules

- No slice issues and no code before approval.
- The spec is the source of truth; issues link to its sections instead of copying them.
- Update the spec when a decision changes during the build — a stale spec is worse than none.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-feature` | Approved `spec.md` with a posted spec-level design review | `feature-to-issues` or `file-feature`, then the docs PR (`create-pr`) |
