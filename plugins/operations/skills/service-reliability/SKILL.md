---
name: service-reliability
description: "Define and verify service performance, reliability and capacity. Use for SLOs, latency/load, overload handling, observability or reliability improvements."
license: MIT
metadata:
  version: "1.0.0"
---

# Service Reliability

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. Define user-visible objectives

Choose SLIs with numerator/denominator, measurement window, exclusions and data quality. Set SLOs/error budgets from user harm and business constraints. Separate successful acceptance from completed delivery; unknown outcomes stay visible.

## 2. Model workload and capacity

Define arrival rate, concurrency, payload/data distribution, hot keys, read/write mix, think time and dependencies. Measure p50/p95/p99, throughput, error rate, saturation, queue age and resource cost. Warmup, sample size and variance matter; three medians do not establish tail behavior.

## 3. Protect overload and failure paths

Use bounded queues/concurrency, timeouts, cancellation, backpressure and retry budgets. Avoid retry amplification. Cache correctness includes tenant identity, invalidation, freshness and stampede control. Degrade only within explicit product/security constraints.

## 4. Observe and improve

Link metrics, traces and safe logs to a revision and request/work identity where permitted. Alert on user-impacting burn rates and actionable failure modes with owners/runbooks. Compare before/after under equivalent workloads; optimize a measured bottleneck, not a guessed one.

## Verification and report

Run representative baseline/candidate comparisons, saturation/recovery, dependency timeout, retry storm and cancellation tests. Verify alerts fire and recover using synthetic signals without paging unrelated teams.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Do not improve latency by weakening authorization, durability or correctness.
- Never claim production capacity from a toy workload.
- Monitoring must not leak payloads or create unbounded metric cardinality.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
