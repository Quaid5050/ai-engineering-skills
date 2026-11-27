---
name: spec
description: "Write and get approval for a feature spec — problem and users, designs and states, numbered must/should/could requirements with checkable acceptance criteria, API contract with who may call what, data and migration risk, client and platform/background behaviour, safety failure modes and privacy rules each becoming criteria, analytics, performance budgets, rollout and rollback, risks and open questions — reviewed by a fresh agent and always design-reviewed by the architect agent before approval. Use for anything multi-area, schema-changing, safety-critical or privacy-relevant. Trigger on /spec, 'write a spec', 'spec this feature', 'PRD', 'technical design for', 'plan this feature'."
argument-hint: "[feature name, MVP id, or spec folder]"
license: MIT
metadata:
  version: "2.0.0"
---

# Spec

Write the spec for `$ARGUMENTS` at `docs/specs/<NNN>-<slug>/spec.md` — the same folder and docs branch (`docs/<docs-issue>-<slug>`) `investigate-feature` created. If `$ARGUMENTS` is empty, ask which feature. A small, clear change goes straight to `file-feature`.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

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

Use `design-review` for high-risk or costly-to-reverse decisions and whenever project policy requires it. Reuse the existing task/spec revision and review location; create a provisional epic only when needed for coordination and already authorized. Standard plans can receive a focused design assessment within the ordinary review. Review changed risks without repeating unchanged assessments.

**Gate:** applicable review evidence is recorded; no unresolved blocking finding. Record why independent pre-change review is or is not required.

## 4. Approval

Show requirements, material risks and unresolved decisions. Reuse explicit approval already covering this spec/scope; ask only where a material product decision remains. Record the approval source and revision. Then:
- multi-slice → `feature-to-issues` when tracker coordination is needed; otherwise keep the agreed slice plan on the existing branch;
- one clear authorized slice → `implement`; use `file-feature` if tracking policy requires it.

Pin the spec revision used for implementation. A separate docs PR is optional unless project policy requires it.

## Rules

- Resolve material scope decisions before dependent implementation; do not request the same approval twice.
- The spec is the source of truth; issues link to its sections instead of copying them.
- Update the spec when a decision changes during the build — a stale spec is worse than none.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-feature` | Approved scope/spec revision with risk-appropriate review | `implement`; tracking and separate docs PR only as needed |
