---
name: recovery-drill
description: "Plan and exercise incident recovery, backup restore and continuity. Use for disaster recovery, failover drills or incident readiness."
license: MIT
metadata:
  version: "1.0.0"
---

# Recovery drill

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Scope the drill

Name assets, dependencies, owners, RPO/RTO, allowed environment and abort conditions. Separate a simulation from an actual disruptive test. Capture safe baseline health and rollback access before starting.

## 2. Recover deliberately

Test restoration of data plus keys, identities, configuration, artifacts and dependent services. Validate schema/application compatibility and business invariants after restore. Failover includes routing, client retries, replication lag and split-brain prevention; failback is a separate tested path.

## 3. Coordinate an incident

For a real incident, assign command, technical and communication ownership; record decisions and timeline. Authorized reversible containment may precede ordinary tracker ceremony. Preserve forensic evidence with restricted access; do not destroy logs or rotate credentials without considering containment/recovery needs.

## 4. Learn from evidence

Report actual recovery time/data loss, failed assumptions and remaining gaps. Analyze causal contributors without inventing a single root cause. Give follow-up controls owners, deadlines and an effectiveness check.

## Verification and report

Execute the authorized restore/recovery path, compare observed RPO/RTO with targets and prove recovery checks catch incomplete restoration. If execution is unavailable, deliver a plan labeled unexercised.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never run destructive drills in production without explicit authorization.
- Preserve sensitive incident evidence securely.
- Do not close follow-up work solely because a document was written.

## Composition

| From | This skill | To |
|---|---|---|
| `incident`, `postmortem` (lifecycle); `database-operations`, `service-reliability` | Measured recovery against targets, gaps recorded | `postmortem`, `file-bug` (lifecycle); `capture-lesson` (meta) |
