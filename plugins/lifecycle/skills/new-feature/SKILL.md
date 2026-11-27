---
name: new-feature
description: "Deliver a feature with a risk-based workflow and relevant verification. Use when asked to build a feature end to end; route small changes directly and reserve separate specifications/reviews for justified risk."
argument-hint: "[feature name, MVP id or design frame]"
license: MIT
metadata:
  version: "2.0.0"
---

# New feature

Deliver the feature in `$ARGUMENTS` within the user's scope. Route only to applicable procedures; do not turn a small change into a full project lifecycle.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

Reuse `work-context` (foundation plugin): outcome, actual commands, relevant code, existing decisions, permissions and risk tier. Missing product decisions are raised once; independent discovery can continue.

## 1. Choose the shortest sufficient route

| Tier | Route |
|---|---|
| Quick | Inspect the affected code, implement the bounded change, targeted checks and diff review. |
| Standard | Short plan/acceptance criteria, relevant specialist guidance, implementation with meaningful tests, one focused review and required checks. |
| High-risk | Written design/failure/threat model, independent design review where available, failure/recovery/compatibility tests and deployment-readiness evidence. |

Use `investigate-feature` when requirements or existing behavior are unclear. Use `spec` when coordination, uncertainty or irreversible choices justify a durable design. Use `feature-to-issues` for genuinely independent slices. Reuse an existing issue/request; create a tracker item or separate docs PR only when requested or required by the project.

## 2. Implement and verify

Use `implement` for the selected scope. Load only relevant backend/mobile/web/AI/data/desktop/systems procedures. Keep a single owner for each output; parallelize independent checks where supported. Reuse prior passing evidence while its inputs remain unchanged.

Resolve applicable security and deploy-readiness findings before declaring merge eligibility. A code review may begin earlier as provisional; a missing future verdict is pending evidence, not automatically a code defect. Deployment readiness does not authorize a deployment.

## 3. Deliver the requested state

Commit, push, open a PR, merge or release only within existing authorization and project policy. A request to build a feature is not permission to deploy it. Explicit no-merge instructions remain binding even when every gate passes.

## Rules

- Preserve security and meaningful verification; remove duplicate ceremony rather than required controls.
- Risk is determined by impact and uncertainty, not file count.
- Do not require speculative abstractions or unrelated cleanup.
- Report implemented, verified and pending work separately.

## Composition

| From | This skill | To |
|---|---|---|
| A feature request | Proportionate scope and routing | `implement`, applicable specialists, `create-pr` when authorized |
