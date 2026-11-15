---
name: new-feature
description: "Take one feature from idea to a merged PR as vertical slices by chaining the lifecycle skills — investigate, size it, spec with a spec-level design review + epic + sub-issues (non-trivial) or one issue (small), the docs PR, start the riskiest slice, slice-level design review posted before production code, build test-first through implement, then pre-commit, PR, independent code review with design pass, CI, deploy check and the merge gates — with a gate after each step. The one-command entry point. Trigger on /new-feature, 'build the X feature', 'implement feature X', 'add feature', 'build screen X', 'idea to PR'."
argument-hint: "[feature name, MVP id or design frame]"
license: MIT
metadata:
  version: "1.0.0"
---

# New feature

Take `$ARGUMENTS` (a feature name, an MVP id like `B2`, or a design frame) from idea to merged slices. This skill only routes; each step's rules live in the skill it calls. If empty, ask which feature.

## 0. Read the project

`AGENTS.md`: tracker, milestones, commands, merge gates and the project's optional policies, the safety-critical list. No `AGENTS.md`, conventions or CI at all → offer `bootstrap-project` first; building features in a repository with no rules teaches agents whatever the first file does.

## Steps

| # | Step | Skill | Skip when |
|---|---|---|---|
| 1 | Docs issue, then investigate: design (or a state table + low-fidelity flow), brief, MVP scope, existing code → build pack | `investigate-feature` | A build pack already exists |
| 2 | Size it (test below) | — | — |
| 3a | Non-trivial: spec → spec-level design review (architect, on the epic) → approval → epic + sub-issues → docs PR | `spec`, `design-review`, `feature-to-issues`, `create-pr` | Small |
| 3b | Small, one slice: one issue, then the docs PR for the investigation | `file-feature`, `create-pr` | Non-trivial |
| 4 | After the docs PR is merged, pick up the first (riskiest) slice: branch from the issue, plan | `start-issue` | — |
| 4a | **Slice-level design review, posted on the slice issue before production code** | `design-review` (architect agent) | **Never** — not for speed, not for small slices |
| 5 | Build and verify test-first, following the design review | `implement` (feature mode) | — |
| 6 | Commit → open the PR → independent code review with design pass, posted on the PR | `pre-commit`, `create-pr`, `code-review` (reviewer agent) | — |
| 7 | CI green → deploy check → device tests | `ci`, `deploy-check`, `device-test` (mobile plugin) | Device tests: no device-relevant change, or listed open when the project batches them before release |
| 8 | Merge gates → merge | `merge` | — |
| 9 | Next slice | back to 4 | No slices left |

Step 3 is **never skipped**: no production code before the issue(s) exist in their milestone, and step 4 creates the branch from the issue.

**Size test (step 2)** — non-trivial if any is true: it touches two or more of client / platform / server / data; it adds or changes a table; it adds a scheduled job, notifications or file uploads; it touches a path on the project's safety-critical list; it changes who can see whose data; the build pack has an unresolved product question.

## Gates

- After 1: show the build pack summary and open questions. Product questions are the owner's.
- After 3: issues exist only after the owner approved the breakdown; the spec-level review is posted; the docs PR is open (merged before step 4).
- After 4a: no production code until the slice's design review is on the issue and every design finding is resolved in the plan.
- After 5: every acceptance criterion has evidence; device tests done or listed as open.
- After 7: the `merge` gates hold — not "tests are green".

## Rules

- One slice = one branch = one PR; never stack several slices in one PR.
- Follow the filed order (riskiest first) unless the owner changes it.
- **The speed rule:** going faster may reduce test reruns and review rounds, never the tests written, the design review or the design pass. Every brief you give a subagent for this work names both as required.

## Composition

| From | This skill | To |
|---|---|---|
| `shape-idea`, `bootstrap-project`, the owner | Routes the whole feature | Every lifecycle skill above, in order; `release` when the milestone ships |
