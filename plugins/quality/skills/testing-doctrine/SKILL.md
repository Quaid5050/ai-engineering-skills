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

Inspect the changed behavior, existing test layers, fixtures, supported environments and actual commands. Select tests by risk and boundary. Read only the relevant `write-tests` reference.

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

**Default: fake only what a test cannot run**, shaped like the real interface — the default boundaries table is in [references/boundaries-and-types.md](references/boundaries-and-types.md); the project's own table, when it has one, is the complete list. A double of owned code is allowed only when isolating that boundary is the purpose of the test, never to make a test easier to write. Avoid interaction assertions that merely mirror implementation. Verify doubles against actual boundary behavior with separate integration/contract tests. A storage emulator may differ from the provider; document unsupported semantics. Integration tests must use the relevant real engine for behavior the double cannot establish.

## 3. Safety-critical code: failure paths first

For anything where a silent failure can harm a person, lose money or lose or corrupt data, write the failure-path tests **before** the happy path:

- no network → queued, retried, delivered later, or the person is told it failed;
- process killed or restarted mid-flow → state survives;
- permission revoked or downgraded → surfaced, not silent;
- server error, timeout or lost acknowledgement → bounded retry with the same idempotency identity, then a fallback or a visible failure;
- duplicate or out-of-order events → one logical effect, **always paired** with tests that dedupe does not swallow real events: a genuine second event still fires, a late event after reconnect is still delivered (marked late);
- timer boundary → fires at exactly the limit, not one tick before or never.

Which paths are safety-critical is **the project's list**; a path missing from it is raised with the owner, not guessed. Each test asserts the effect still happens **or** the failure is visible to someone — "nothing happened and nobody knows" is the bug these tests catch.

## 3a. Prove important tests detect failures

For new behavior or a bug regression, observe a meaningful failure before the fix when practical. Characterization may start green. For high-impact invariants, inject the relevant fault or targeted mutation and record that the assertion fails; restore the implementation afterward. Do not mutate a shared working tree that others are using: use an isolated fixture/worktree.

Cover both sides and equality at time/size boundaries. For delivery, test persisted recovery and provider acceptance with lost acknowledgement; deduplication is not a delivery guarantee.

## 4. Control flakiness and cost

Run focused checks while editing and required integration/build checks before submission. Reuse passing evidence until relevant inputs change. Use bounded condition waits rather than unexplained sleeps. Separate environmental failures from product failures; a retry may diagnose flakiness but must not silently turn it into a clean result.

Quarantine only with owner, reason, expiry, visible reporting and compensating coverage for critical behavior. Do not delete a regression just to make CI green. Parallel tests need isolated data/resources and deterministic cleanup.

## 5. Report coverage honestly

Map acceptance criteria and risks to tests and unverified cases. Line/branch coverage can expose gaps but is not proof of correctness; use targeted mutation and requirement coverage where valuable. There is no universal 100% threshold.

Report command, environment, source revision, results and limitations. Use synthetic data; never copy real personal records into fixtures or output.

## 6. The rungs (the one ladder other skills point to)

Where a class of mistake can be caught, usually earliest and cheapest first:

**type / compile → lint → architecture test → unit / integration test → CI → design review → code review → device test → alert / monitoring → user report**

Choose the earliest *effective* guard; the order is a default, not a law (a threat review can precede any code). State where a defect was found and which specific guard could prevent or detect recurrence.

## Reject on sight

Expected values computed with the production formula · skipped or commented-out tests · tests that pass whether or not the feature works · mocks of owned code used only for convenience · retries that turn a flaky test green · asserting "not null" when the point was a value · unexplained fixed sleeps · real personal data · a safety-critical change without a failure-path test. Test types (unit, integration, end-to-end, smoke, regression, device) and when each runs: [references/boundaries-and-types.md](references/boundaries-and-types.md).

## Rules

- Never weaken an assertion or remove a valid test merely to accept a regression.
- A passing mock/model test does not establish provider, device or production behavior.
- High-risk paths need failure/recovery evidence; missing equipment is reported as unverified.

## Composition

| From | This skill | To |
|---|---|---|
| Implementation, review, regression investigation | Risk-based test strategy and evidence | `write-tests`, `tdd`, applicable specialist verification |
