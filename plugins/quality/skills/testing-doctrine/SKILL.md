---
name: testing-doctrine
description: "The rules every test follows on any stack, and why — arrange/act/assert, one behaviour per test, hard-coded expected values, no logic in tests, exact assertions including absence, behaviour not implementation, fakes only at real boundaries (clock, vendors, OS), real database in integration tests, failure paths first for safety-critical code, prove the test can fail, deterministic time, synthetic data. Read by tdd, write-tests, implement and code-review. Use when writing, reviewing or judging tests. Trigger on 'testing rules', 'how should this be tested', 'is this a good test', 'should I mock this', 'flaky test', 'test doctrine'."
argument-hint: "[test, test file or question]"
license: MIT
metadata:
  version: "1.0.0"
---

# Testing doctrine

The **what and why** of tests. `write-tests` owns the commands and folders; `tdd` owns the red-green-refactor loop. A test that breaks a rule below is broken even if it passes. Apply it to `$ARGUMENTS` (a test, a test file, or a question). If empty, apply it to the tests in the change in hand.

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` and any testing guide (`docs/testing*`).
2. Find the project's **boundary fakes table** (what tests may fake) and its integration-test setup (how a real database or service is started for tests).
3. If the project has no fakes table, use the generic rows in §2 and offer to record the project's version in its testing guide.

The project wins on facts (commands, fixtures, folders); these rules win on what makes a test trustworthy. A project rule that weakens them is raised with the user, not silently followed.

## 1. The invariants

**Arrange, act, assert.** Three visible parts, one action. A test that acts twice is two tests.

**One behaviour per test, named for it.** `rejects_an_order_with_more_than_50_lines`, `'shows "Out of stock" when quantity is zero'`. When it fails, the name alone says what broke.

**Hard-code every value.** Inputs and expected outputs are literals. No current-time reads, no randomness, no expectation computed with the same formula as the code:

```text
good: expect(total(lines), 4250)                 # 42.50 in cents, worked out by hand
bad:  expect(total(lines), sum(l.price * l.qty)) # repeats the implementation's maths
```

**No logic in a test body.** No `if`, loops or `try/catch`. Several cases → the framework's parameterised tests, or a table of cases with one test each.

**Exact assertions.** `equals 3`, not `> 0`; exactly one element, not "some"; the exact error type and code. Assert side effects (which row, which message, to whom) **and absence**: the forbidden caller got nothing, the retried request did not create a second order, the cancelled job sent no email.

**Test behaviour, not implementation.** Assert what a person or caller can observe: rendered text, returned body, stored row, sent message. Never private fields or call order. A refactor that keeps behaviour keeps the tests green.

## 2. Fakes only at real boundaries

Never mock code you own (domain, use cases, repositories, view models) — no call-verification of your own classes. Use the real implementation, injected through the constructor or the DI container. A UI or view-model test may replace a repository with an **in-memory implementation of the repository interface** (a real-shaped fake that stores and returns data); the repository's own logic is tested against a fake transport.

Fake **only** what a test cannot run, and keep the fake shaped like the real interface:

| Boundary | Fake |
|---|---|
| Time | Injected clock with a fake that tests set and advance |
| OS / device (location, camera, sensors, permissions) | A fake of the bridge interface with scripted answers |
| Outbound vendors (email, SMS, push, payments, maps) | A recording sender: tests assert the message and the recipient |
| HTTP from a client app | A transport fake returning recorded real responses |
| Identity providers (OTP sender, token signing keys) | A development provider / fake key source |
| Object storage | **Not faked:** a real S3-compatible engine in a container (or the provider's local emulator), a fresh bucket per test class |

The project's table is the complete list of allowed fakes; other skills refer to it.

**Databases and caches are not faked in integration tests.** Run the real engine (local services or a disposable instance), give each test class its own fresh, migrated database or schema, seed and clean its own data. CI runs the same engine version.

**Gate:** every fake in the change is in the boundaries table; nothing you own is mocked.

## 3. Safety-critical code: failure paths first

For anything where a silent failure can harm a person, lose money or lose or corrupt data, write the failure-path tests **before** the happy path:

- no network → queued, retried, delivered later, or the person is told it failed;
- process killed or restarted mid-flow → state survives;
- permission revoked or downgraded → surfaced, not silent;
- server error or timeout → bounded retry, then a fallback channel or a visible failure;
- duplicate or out-of-order events → one effect, not two — **always paired** with tests that the dedupe does not swallow real events: a genuine second event still fires, and a late event after reconnect is still delivered (marked late);
- timer boundary → fires at exactly the limit, not one tick before or never.

**Which paths are safety-critical is the project's list** (in `AGENTS.md`). Typical candidates — alerts, payments, scheduled reminders, background sync, offline submissions, account recovery — are examples only; the project's list wins, and a path missing from it is raised with the owner rather than guessed.

Each asserts the effect still happens **or** the failure is visible to someone. "Nothing happened and nobody knows" is the bug these tests exist to catch.

## 4. Prove the test can fail

A green test is evidence only if it can go red. When a test guards a specific mistake, make that mistake (flip `>` to `>=`, drop the authorisation check, remove the retry), watch it fail for the right reason, revert. Make sure the broken line is on the path the assertion reads. Boundary tests use data past the boundary (16 minutes old for a 15-minute rule, not exactly 15).

A characterisation test (pinning existing behaviour before a refactor) may pass first time — say so in its name or a comment, and still do the break-it check. Never pin behaviour you believe is wrong.

**Gate:** each guard on a safety-critical path has a recorded break-it check.

## 5. Determinism

- Fast (unit tests in milliseconds), isolated (each test owns its data), repeatable (same result every run, any timezone — run once with `TZ` set to a far timezone such as `Pacific/Auckland` when time logic changes), self-validating.
- A flaky test is a broken test: fix it or delete it. Never retry until green.
- Wait for conditions with bounded polling, never fixed sleeps. Endless animations never "settle": disable animations in tests or pump a fixed duration.

## 6. Data

Synthetic but realistic: "Customer A", "Shop B", generated UUIDs, obviously fake coordinates and phone numbers from reserved ranges. Never real homes, names, emails or phone numbers. Production *shapes*, never production *records*.

## 7. Integration tests

Drive the real entry point (HTTP endpoint, job, message consumer), the real database, seed and clean your own data, idempotent; assert isolation: a user of tenant A never sees tenant B's data, and a forbidden caller gets the project's stated status.

## 8. The rungs (the one ladder other skills point to)

Where a class of mistake can be caught, earliest and cheapest first:

**type / compile → lint → architecture test → unit / integration test → CI → design review → code review → device test → alert / monitoring → user report**

Every finding, postmortem and lesson names the rung that caught it and the earliest rung that *should* have. Moving a class of problem one rung earlier beats fixing one more instance. `code-review`, `investigate-bug` and `postmortem` (lifecycle plugin) and `capture-lesson` (meta plugin) use this ladder.

## Reject on sight

Calculated expectations · skipped or commented-out tests · tests that pass whether or not the feature works · mocks of your own code · branching or loops in tests · retries for flakiness · asserting "not null" when the point was a value · fixed sleeps · real personal data · a safety-critical change without a failure-path test.

## Rules

- These rules apply to every test in every layer, including tests written by agents.
- Never weaken or delete a test to make a change pass; if the test was wrong, say why in the change.
- A rule that turns out wrong for a project is changed in the project's testing guide (and here via `capture-lesson`, meta plugin), not ignored.

## Composition

| From | This skill | To |
|---|---|---|
| `tdd`, `write-tests`, `implement` (lifecycle), `code-review`, the `tester` agent (agents plugin) | The rules a test must meet | `write-tests` for commands and folders; `tdd` for the loop |
