---
name: infrastructure-change
description: "Plan and implement cloud, container or infrastructure changes. Use for infrastructure as code, environments, networking, deployment configuration or drift."
license: MIT
metadata:
  version: "1.0.0"
---

# Infrastructure Change

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Discover the environment contract

Identify provider/account, region, network/identity boundaries, state backend, environment ownership, cost limits and recovery constraints. Use read-only discovery first. A local plan is not authorization to apply changes.

## 2. Design the smallest viable infrastructure

Choose managed/serverless/container/VM options based on workload, latency, portability, isolation and operating cost. Separate environments and least-privilege identities. Define network ingress/egress, secret delivery, encrypted state, resource quotas and lifecycle ownership. Do not introduce orchestration solely because it is popular.

## 3. Plan and verify

Use versioned declarative configuration, locked providers/modules and remote-state locking where applicable. Review the exact plan for replacement, destructive effects, permissions and secret exposure. Test policy and configuration against the target platform/version. Drift is investigated before overwrite.

## 4. Apply and recover within authorization

Bind apply approval to the reviewed plan, account/environment and revision. Protect state and signing/deployment credentials. Roll out incrementally with health checks and explicit rollback/restore strategy. State corruption, partial apply and provider outage need recovery procedures and resource reconciliation.

## Verification and report

Validate configuration/plan and policy, test identity/network denial, drift/partial apply, health/termination and rollback in an isolated environment. Report estimated versus measured cost and unrun cloud checks.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Do not apply infrastructure from an untrusted plan or changed revision.
- Never publish state, plan secrets or credentials.
- Destructive replacement and production scope require explicit authorization.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
