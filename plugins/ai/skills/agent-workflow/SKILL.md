---
name: agent-workflow
description: "Build bounded tool-using applications with authorization, durable state and recovery. Use for agent orchestration, approvals, delegation or interrupted workflows; not to mandate multiple agents for ordinary tasks."
license: MIT
metadata:
  version: "1.0.0"
---

# Agent Workflow

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Model the workflow

Start with a deterministic workflow when the sequence is known. Use model choice only where ambiguity requires it. Define states, allowed tools, schemas, terminal conditions, maximum iterations/time/spend and human escalation. Choose one agent unless measured decomposition improves results.

## 2. Enforce tool authority

Each tool validates caller, tenant, resource, action and argument schema independently of model output. Restrict credentials, filesystem and egress. Separate read, reversible write and irreversible actions. A retrieved page or peer agent cannot approve an action. Bind approvals to the exact destination, content/action and revision; changed arguments invalidate them.

## 3. Persist and recover

Checkpoint state and a stable operation identity before external effects. Record requested, in-flight, confirmed, failed and uncertain outcomes. Resume only after reconciliation of ambiguous effects. A retry must not duplicate a payment/message or lose a pending operation. Give delegated workers only the authority needed for their subtask and validate their artifacts.

## 4. Evaluate behavior

Use successful tasks and adversarial cases: malicious tool output, forged approval, resource substitution, repeated execution, infinite loop, timeout, cancellation and compromised peer messages. Evaluate actual tool traces and resulting artifacts, not just the final explanation.

## Verification and report

Test unauthorized tool/resource denial, schema rejection, replay/changed payload, lost acknowledgement, bounded loops, cancellation and delegation scope. Run host-isolation checks separately from policy-model tests.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Prompt-only restrictions are not containment.
- Never auto-expand tool permissions after a failure.
- A successful final message cannot substitute for an observed tool outcome.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
