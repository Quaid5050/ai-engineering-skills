---
name: concurrency-networking
description: "Design and troubleshoot concurrent and networked systems. Use for races, cancellation, deadlocks, sockets, protocol parsing or bounded resource handling."
license: MIT
metadata:
  version: "1.0.0"
---

# Concurrency Networking

Deliver the requested artifact in `$ARGUMENTS`; do not create infrastructure, accounts or unrelated migrations merely because this procedure mentions them.

## 0. Read the project

Reuse `work-context` and `safe-agent-execution` (foundation plugin). Read the current implementation, actual commands, supported versions and constraints. Load only the applicable parts of [the reference](references/implementation.md). Treat unavailable platform execution as unverified.

## 1. State invariants and failure model

Identify shared state, ownership, synchronization, ordering, cancellation and resource limits. Separate wall time, monotonic elapsed time and distributed ordering. Define what happens under partial reads/writes, disconnects, partitions, timeouts and process death.

## 2. Choose coordination deliberately

Prefer ownership/message passing or simple locking before lock-free complexity. Document lock ordering, critical sections and visibility guarantees. Atomics need a precise memory-order argument. Cancellation propagates to owned tasks and resources; joining/shutdown has a deadline and observable unfinished work.

## 3. Bound networking and work

Validate protocol framing and lengths; handle partial I/O and EOF. Use timeouts for connection, request and idle phases, concurrency limits, bounded queues and backpressure. Authenticate peers and verify transport identities. Retries need idempotency and jitter; do not retry an ambiguous side effect blindly.

## 4. Diagnose and measure

Use traces, thread/task dumps, race tools and controlled scheduling. Benchmark representative contention, tail latency and resource saturation. A passing stress test is not proof of race freedom; retain minimal interleaving reproductions.

## Verification and report

Exercise deterministic interleavings, timeout/cancellation, deadlock order, partial I/O, exhausted queues and shutdown. Measure latency distribution under representative load and record environmental limits.

Report the artifact, decisions, commands/results, revision, environment and remaining uncertainty. Documentation or a local model is not evidence of production or device behavior.

## Rules

- Do not equate scheduler timing with a correctness guarantee.
- Avoid unbounded task creation, buffers or retries.
- A process-local primitive does not protect a distributed invariant.

## Composition

| From | This skill | To |
|---|---|---|
| An applicable engineering task | Scoped implementation and acceptance evidence | Relevant tests, security review and deployment readiness; external actions only when authorized |
