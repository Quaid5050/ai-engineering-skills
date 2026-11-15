---
name: tdd
description: "Build a behaviour test-first, one test at a time — pick the next behaviour from the test list, write one failing test and see it fail for the expected reason, write the least code to pass, refactor while green, commit, repeat; with the signals that mean the design is wrong and the few allowed exceptions. Use when implementing any behaviour change. Trigger on /tdd, 'test first', 'red green refactor', 'TDD this', 'write the failing test first', 'build this test-driven'."
argument-hint: "[behaviour, acceptance criterion or issue]"
license: MIT
metadata:
  version: "1.0.0"
---

# TDD

Build `$ARGUMENTS` (a behaviour, an acceptance criterion, or an issue) one test at a time. Rules for the tests themselves: `testing-doctrine`. Commands and folders: `write-tests`. If `$ARGUMENTS` is empty, take the next item from the current issue's "Tests to write first".

## 0. Read the project

1. Read `AGENTS.md` / `CLAUDE.md` for the test commands, especially how to run **one** test.
2. Read the issue or spec: the acceptance criteria and its test list are the order of work.
3. Read the code around the change and the conventions for its layer (`engineering-principles`, lifecycle plugin, and the stack conventions skill).

**Gate:** you can run a single test in this project and you have an ordered test list.

## 1. The loop

1. **Pick the next behaviour** from the test list: the issue's tests first, then edges, then errors; for safety-critical code the failure paths first (`testing-doctrine` §3). One behaviour only.
2. **RED.** Write one test. Run only that test. It must fail **for the reason you expect** — an assertion on the missing behaviour, not an unintended compile error, a missing fixture or a typo. Paste the failure line.
   - A compile error is an acceptable first red only when the type or function genuinely does not exist yet; add the empty shell and run again until the failure is the assertion.
3. **GREEN.** Write the least code that makes this test pass. Hard-coding is fine if the next test will force the general solution. Run the test, then the rest of the file.
4. **REFACTOR.** With everything green: remove duplication, name things, move rules out of edges into the domain, keep behaviour. Run the area's tests after each step. No new behaviour during refactor.
5. **Commit** when a meaningful behaviour is done (`pre-commit`, lifecycle plugin), then back to 1.

**Gate (every cycle):** the red output was the expected assertion, and the green run passed the single test and its file.

## 2. Stop and rethink when

- A test is hard to write → the design is telling you something (too many dependencies, logic in an edge). Fix the design, not the test.
- You want to mock your own class → inject the real one; fake only the boundaries in `testing-doctrine` §2.
- Green needs a lot of code at once → the test is too big; split the behaviour.
- A test passes immediately → it is not testing new behaviour, or the behaviour already exists. Do the break-it check from `testing-doctrine` §4.

## 3. Exceptions

- **Characterisation tests** before a refactor may pass on the first run — label them.
- **Pure layout from a design:** a UI test per state's content and accessibility first; the visual match is checked with screenshots after (`design-to-screen`, mobile plugin; `add-web-page`, web plugin).
- **Platform code that cannot run in CI:** test the portable logic test-first; write the device steps before the platform change and run them after (`device-test`, mobile plugin).
- **Config, docs, generated code:** no manufactured failing test; use their own checks.

## Rules

- Never write several tests and then all the code. Never write code without a red test asking for it.
- Never change a test to match the code unless the test was wrong — and say why.
- Keep the loop fast: run the single test, not the whole suite, during red/green.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `bugfix` (lifecycle plugin) | One behaviour at a time, red → green → refactor | `pre-commit` (lifecycle) per finished behaviour; `write-tests` for commands; `testing-doctrine` for the rules |
