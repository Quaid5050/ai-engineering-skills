---
name: testing-doctrine
description: "Choose meaningful tests by risk, boundaries and observable invariants. Use when writing or reviewing tests, investigating flakiness or planning verification; includes property, sequence, integration and failure-path testing."
argument-hint: "[test, test file or question]"
license: MIT
metadata:
  version: "2.0.0"
---

# Testing doctrine

Choose tests that expose the failure modes of `$ARGUMENTS`. Test quality comes from independent oracles, meaningful coverage and reproducible failures, not a single permitted test shape.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

Reuse the current `work-context` (foundation plugin). Inspect the changed behavior, existing test layers, fixtures, supported environments and actual commands. Select tests by risk and boundary. Read only the relevant `write-tests` reference.

## 1. Make assertions trustworthy

Use arrange/act/assert where it clarifies the example. Keep one coherent behavior or invariant per test; sequences and repeated calls are essential for retries, state transitions and idempotency. Prefer explicit expected examples, independent reference implementations or invariant/metamorphic oracles; never duplicate the production formula as the only expected result.

Parameterization, loops, generated inputs and property/state-machine tests are valid. Retain the failing seed/example and shrink the counterexample. Use fixed clocks or controlled time sources. Assert exact values when the contract is exact, tolerances when numerical error is specified, and distributions with justified statistical criteria when behavior is probabilistic.

Assert meaningful positive effects and absence: forbidden callers receive no data, cancellation does not commit, retries do not create a second logical entity, and a genuine new operation still succeeds. Internal call order matters only when it is part of a real protocol or resource contract.

## 2. Choose boundaries and layers

| Layer | Evidence |
|---|---|
| Unit/property | Pure rules and state invariants; deterministic dependency doubles where justified |
| Integration | Actual database/cache/transport semantics, migrations, authorization and cleanup using isolated synthetic data |
| Contract/compatibility | Wire schemas, old clients, provider assumptions, event replay and backward compatibility |
| End-to-end | A small set of critical journeys through deployed boundaries and real configuration |
| Fault/concurrency | Crash windows, races, cancellation, leases, out-of-order events, resource exhaustion and recovery |
| Security/accessibility/performance | Applicable negative controls, assistive/manual checks and representative measured workloads |

Use test doubles to isolate a meaningful boundary, even for owned code when isolation is the purpose. Avoid interaction assertions that merely mirror implementation. Verify doubles against actual boundary behavior with separate integration/contract tests. A storage emulator may differ from the provider; document unsupported semantics. Integration tests must use the relevant real engine for behavior the double cannot establish.

## 3. Prove important tests detect failures

For new behavior or a bug regression, observe a meaningful failure before the fix when practical. Characterization may start green. For high-impact invariants, inject the relevant fault or targeted mutation and record that the assertion fails; restore the implementation afterward. Do not mutate a shared working tree that others are using: use an isolated fixture/worktree.

Cover both sides and equality at time/size boundaries. For delivery, test persisted recovery and provider acceptance with lost acknowledgement; deduplication is not a delivery guarantee.

## 4. Control flakiness and cost

Run focused checks while editing and required integration/build checks before submission. Reuse passing evidence until relevant inputs change. Use bounded condition waits rather than unexplained sleeps. Separate environmental failures from product failures; a retry may diagnose flakiness but must not silently turn it into a clean result.

Quarantine only with owner, reason, expiry, visible reporting and compensating coverage for critical behavior. Do not delete a regression just to make CI green. Parallel tests need isolated data/resources and deterministic cleanup.

## 5. Report coverage honestly

Map acceptance criteria and risks to tests and unverified cases. Line/branch coverage can expose gaps but is not proof of correctness; use targeted mutation and requirement coverage where valuable. There is no universal 100% threshold.

Report command, environment, source revision, results and limitations. Use synthetic data; never copy real personal records into fixtures or output.

## 6. Prevention and detection layers

Choose the earliest effective and proportionate guard: design/threat review, types, lint, architecture checks, unit/property/integration tests, CI, code review, device/manual testing and production monitoring. This is not a fixed chronological or cost ranking. State where a defect was found and which specific guard could prevent or detect recurrence.

## Rules

- Never weaken an assertion or remove a valid test merely to accept a regression.
- A passing mock/model test does not establish provider, device or production behavior.
- High-risk paths need failure/recovery evidence; missing equipment is reported as unverified.

## Composition

| From | This skill | To |
|---|---|---|
| Implementation, review, regression investigation | Risk-based test strategy and evidence | `write-tests`, `tdd`, applicable specialist verification |
