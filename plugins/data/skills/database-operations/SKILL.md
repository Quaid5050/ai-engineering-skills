---
name: database-operations
description: "Operate and optimize persistent databases safely. Use for query tuning, isolation/locking, replication, backups, restore drills or database incidents."
license: MIT
metadata:
  version: "1.0.0"
---

# Database operations

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Discover workload and recovery goals

Read engine/version, topology, schema, query workload, traffic distribution, retention and access policy. Establish RPO/RTO and performance budgets. Shared-environment access requires authorization and least-privilege sessions; investigation is read-only unless a repair is separately authorized.

## 2. Diagnose before optimizing

Use sanitized query statistics and representative plans. Execution-plan analysis may execute a query; use safe synthetic/local data where needed. Compare selectivity, composite index order, write amplification, locks, deadlocks, connection pools and replica lag. Do not require an index when the optimizer correctly chooses a scan.

## 3. Protect invariants

State transaction/isolation assumptions. Reproduce lost updates, write skew, uniqueness races and lock ordering with synchronized concurrent transactions. Use constraints, locking or optimistic version checks according to the invariant; application prechecks alone do not guarantee correctness.

## 4. Recover and change safely

Test backup restore into an isolated environment, including keys, roles, extensions, migrations and application compatibility. Verify point-in-time recovery and deletion policy where applicable. A backup-success message is not a restore test. Plan failover/failback, split-brain prevention and client reconnection. Keep data repair resumable, audited and bounded.

## Verification and report

Run the relevant isolation/concurrency case, measured query comparison, interrupted migration/backfill and isolated restore verification. Report actual data volume and duration instead of extrapolating from tiny tables.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Never change production data during an unapproved investigation.
- Do not copy real records into public fixtures.
- A replica is not a backup; retained backups still require access/deletion policy.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-bug`, `incident` (lifecycle); `perf-check` (quality); `data-check` (backend) | Diagnosed workload, protected invariants and rehearsed recovery | `add-migration` (backend) for schema changes; `recovery-drill` for restores; `code-review` (quality); `deploy-check` (lifecycle) |
