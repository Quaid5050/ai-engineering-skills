---
name: write-tests
description: "Write the tests for a file, feature, behaviour or diff in this project — list every behaviour (happy, variations, edges, errors; safety failure paths first), pick the lowest level that proves each (unit, integration through the real entry point, UI per state, platform), write them to the testing doctrine, run the single test, then the area, and report red/green evidence and break-it checks. Stack references for common test toolchains. Use when adding tests to new or existing code. Trigger on /write-tests, 'write tests for', 'add tests', 'test this', 'cover this with tests', 'what tests are missing'."
argument-hint: "[file, feature, behaviour, or empty for the branch diff]"
license: MIT
metadata:
  version: "2.0.0"
---

# Write tests

Write tests for `$ARGUMENTS` (a file, a class, a feature or a behaviour). If empty, test the current branch's diff against the main branch. The rules are in `testing-doctrine` — read it first if you have not in this session. This skill is the **how**.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

1. Read `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md` for test commands, test folders and naming.
2. Detect the stack from the manifests and the CI file; open the matching reference for toolchain detail:
   [references/dotnet.md](references/dotnet.md) · [references/python.md](references/python.md) · [references/node.md](references/node.md) · [references/jvm.md](references/jvm.md) · [references/flutter.md](references/flutter.md) · [references/swift.md](references/swift.md).
3. Find the existing helpers before writing new ones: the integration-test host, database fixture, fake clock, recording senders, UI pump helper. Reuse them.

The project's commands and folders win; the reference only fills gaps.

## 1. List the behaviours

From the issue's acceptance criteria, the design's states, or the diff, list every behaviour in this order: happy path → variations → edges (empty, first item, exactly at a boundary, past it, maximum size) → errors (invalid input, forbidden caller, network or server failure). For safety-critical code put the failure paths from `testing-doctrine` **first**.

Skip what is already covered: search the test folders for the behaviour's words.

**Gate:** a written list; each item is one behaviour a caller can observe.

## 2. Pick the level

| Behaviour | Level |
|---|---|
| Pure rule (a limit, a calculation, a state transition, a permission matrix) | Unit test of the domain |
| HTTP contract, authorisation, persistence | Integration test through the real entry point on a real database |
| Background job, timer, consumer | Unit test with a fake clock, plus one integration test through the job's entry point |
| Client logic (formatters, view models, repositories) | Unit test with in-memory repository fakes / transport fakes |
| A screen and its states | UI test per state (content, accessibility labels) |
| Pixel-level look of a key screen | Golden / screenshot test |
| Platform code (background work, widgets, OS bridges) | Native unit test where possible + `device-test` steps (mobile plugin) |

Prefer the lowest level that proves the behaviour; add one integration test per seam.

## 3. Write them

- Follow `testing-doctrine`: clear setup, action and independent oracle; explicit examples, properties or state-machine sequences as appropriate. Avoid reproducing the production algorithm as the expected result.
- Time from the injected clock; never the real clock. Data synthetic.
- Integration tests exercise real internal seams; unit doubles at owned architectural boundaries are acceptable when separate integration tests cover the real collaboration.
- Forbidden callers: the authorisation tests the project defines (`add-endpoint`, backend plugin, says which status each caller gets).
- Golden/screenshot updates only when the change is intended, and look at the image diff before committing.

## 4. Run

1. Run the focused test. New behavior uses red/green; characterization of existing behavior may start green. Demonstrate sensitivity to the relevant defect without manufacturing a failure.
2. Run affected suites and required CI checks. Reuse unchanged evidence for the same candidate; broaden when dependency impact or failures justify it.
3. For each guard on a safety-critical path, do the break-it check from `testing-doctrine`.

**Gate:** meaningful oracle and failure sensitivity established; applicable suites pass, with skipped/environment-dependent checks named.

## 5. Report

Tests added (file → behaviours), the red and green evidence (command + output line), break-it checks done, and what is still untested and why (for example: needs a real device → a `device-test` row).

## Rules

- Never claim "tests pass" without the command and its output.
- No new test helper when an existing one does the job; a new shared helper goes where the project keeps test support code.
- Never weaken an existing test to make the new code pass.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `bugfix` (lifecycle plugin), the `tester` agent (agents plugin), a review finding | Behaviour list → tests at the right level → evidence | `tdd` for the loop; `testing-doctrine` for the rules; `pre-commit` (lifecycle) |
