---
name: implement
description: "Implement a feature, fix or maintenance change with proportionate planning and verification. Use for authorized code changes; preserve existing work and load only affected specialist guidance."
argument-hint: "[issue number, spec slice, investigation report, or scoped request]"
license: MIT
metadata:
  version: "2.0.0"
---

# Implement

Implement `$ARGUMENTS`: an authorized feature, fix or maintenance task. Keep the requested behavior and scope explicit.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

Reuse `work-context` and its risk tier. Inspect current working changes and relevant implementation/tests. Do not overwrite others' work. Use `safe-agent-execution` before running repository commands from an untrusted source.

## 1. Plan only what the task needs

Quick changes need a clear local intent, not a separate document. Standard changes need a short plan and acceptance criteria. High-risk work needs a failure/threat model and required design review. Reuse the current issue/request and existing authorization.

Name the behavior, data or public contract that changes. For maintenance, distinguish behavior preservation from deliberate compatibility changes. Update characterization/tests when justified by changed APIs or seams; never rewrite expectations merely to bless a regression.

## 2. Build in verifiable increments

Use the relevant conventions and specialist skill only for affected areas. Prefer existing boundaries; do not restructure unrelated code. For a behavior change or bug, add meaningful tests and demonstrate the defect where practical. For characterization/generated/text changes, use applicable verification without manufacturing a red test.

Implement, run focused checks and inspect the result. A failure is evidence: diagnose it, then fix or revert the scoped increment deliberately. Do not blindly revert every failing experiment or keep patching without understanding the failure. Use checkpoints for broad changes.

## 3. Verify the candidate

Run the checks required by the project and risk: type/build/lint, relevant unit/integration/contract tests, plus security/accessibility/performance/device checks when applicable. Validate the actual staged/candidate snapshot. Repeat checks only after relevant inputs change or a concern remains unresolved.

Obtain a focused review; high-risk work needs the required independent review. Resolve applicable security and deployment-readiness findings before final eligibility. If equipment or services are unavailable, record pending evidence and do not claim it passed.

## 4. Report and hand off

State changed behavior, important decisions, files, actual command/results and limitations. Commit/push/PR only as authorized. Leave release and merge to their own policy and explicit user constraints.

## Rules

- Never hide failure, silently lose data or broaden permissions to finish.
- Avoid speculative abstractions and unrelated cleanup.
- An external write requires authorization for that destination and scope; reuse authorization already given.

## Composition

| From | This skill | To |
|---|---|---|
| Task, `new-feature`, `bugfix` | Scoped implementation and evidence | `pre-commit`, `create-pr`, relevant readiness checks |
