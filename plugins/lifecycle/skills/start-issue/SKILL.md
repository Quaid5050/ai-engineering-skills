---
name: start-issue
description: "Prepare an issue or direct task with an isolated branch, current context and risk-appropriate plan. Use when starting implementation; an issue is required only by the project or requested workflow."
argument-hint: "[issue number or URL]"
license: MIT
metadata:
  version: "2.0.0"
---

# Start work

Prepare the requested issue or task in `$ARGUMENTS` for implementation.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

Reuse `work-context`. Inspect working-tree status, current/default branches, relevant issue/request and repository policy. Use actual remote/default branch names.

## 1. Establish scope

Read the issue and dependencies when present. Distinguish absent parent information from failed authentication/network requests; do not silently convert tool failures into no dependency. The user request can serve as scope when a tracker is not required. Search before filing a duplicate issue.

## 2. Isolate the change

Reuse a suitable existing branch, or create a task branch/worktree without moving unrelated work. Record the base revision and scope. Never discard or automatically stash others' changes.

## 3. Plan by risk

Quick: affected behavior/files and targeted checks. Standard: short implementation plan and acceptance criteria. High-risk: written failure/threat/compatibility decisions and required independent design review. Do not create a docs PR merely to begin ordinary implementation.

## Rules

- Use the project's required tracker and branch policy; do not invent extra gates.
- Refresh context when the candidate or dependencies change.
- No implementation before a required high-risk review; a regression reproducer can precede the fix.

## Composition

| From | This skill | To |
|---|---|---|
| Issue or direct task | Isolated scope, branch and plan | `implement`, or `design-review` when required |
