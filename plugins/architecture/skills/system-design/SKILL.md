---
name: system-design
description: "Design systems from requirements, workloads and tradeoffs. Use for new service boundaries, scaling plans or costly architectural decisions."
license: MIT
metadata:
  version: "1.0.0"
---

# System design

> Draft skill: generic procedure, no stack references yet. Project rules win.

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Establish constraints and quality attributes

Record users, use cases, workload ranges, latency/availability/durability objectives, data sensitivity, team capacity and cost. Label assumptions and identify the experiment that would reduce important uncertainty.

## 2. Compare viable options

Start with the simplest architecture that meets the constraints. Compare a modular single deployment with independent services only when isolation, scaling, ownership or release cadence justify the operational cost. Draw context/data/trust boundaries and identify state ownership and consistency requirements.

## 3. Design contracts and failure behavior

Specify synchronous/asynchronous interactions, resource limits, idempotency, ordering, transaction boundaries, partial failure, caching and schema evolution. Plan observability, deployment and recovery with the design rather than as a final appendix.

## 4. Record decisions and validate

Use a short decision record with alternatives, evidence, consequences and revisit triggers. Prototype the uncertain high-cost assumption and measure it. Review security and failure paths before irreversible commitments; avoid diagrams that hide undefined protocols.

## Verification and report

Test the critical capacity/consistency/security assumption with a representative prototype or integration fixture. Record actual measurements and alternatives rejected for concrete reasons.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- No universal monolith/microservice/layering recommendation.
- Do not turn hypothetical future features into mandatory abstractions.
- Distinguish constraints, assumptions and measured evidence.

## Composition

| From | This skill | To |
|---|---|---|
| `shape-idea`, `spec`, `investigate-feature` (lifecycle) | Compared options, contracts and failure behavior | `decision` (meta) to record the choice; `threat-model` for new trust boundaries; `service-reliability` for capacity; `design-review`, `feature-to-issues` (lifecycle) |
