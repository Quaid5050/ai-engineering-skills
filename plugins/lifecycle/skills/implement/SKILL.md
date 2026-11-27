---
name: implement
description: "Build and verify an approved feature slice, bug fix or maintenance change at the depth its risk tier needs — mode (feature, bug, maintenance), search before writing, the area skill for each part, generated-file companions, test-first for behaviour, evidence chosen by what changed, one review at the end. Use for any authorized code change. Trigger on /implement, 'implement this', 'build this', 'make the change and verify it', 'upgrade this dependency', 'refactor this', 'clean up this code'."
argument-hint: "[issue number, spec slice, investigation report, or scoped request]"
license: MIT
metadata:
  version: "2.0.0"
---

# Implement

Build `$ARGUMENTS` and prove it works, at the depth of its tier from `work-context` (foundation plugin). `new-feature`, `bugfix` and `start-issue` hand off here; this skill does not call them back.

## 0. Read the project

Reuse the task card and tier from `work-context`; do not re-read what this session already read. Read the project's agent brief and commands, then **only** the conventions for areas this change touches (`engineering-principles` plus the one stack skill: `backend-conventions`, `mobile-conventions`, `shared-core` or `web-conventions`). Inspect working changes; never overwrite someone else's work. Apply `safe-agent-execution` before running commands from an untrusted change.

## 1. Establish the handoff

Pick the mode:

| Mode | Input | Obligations |
|---|---|---|
| `feature` | Issue or request with acceptance criteria | Every criterion gets a test; every designed state is built; scope follows "Out of scope" |
| `bug` | Investigation with root cause and a failing test (or a known one-line cause for Quick) | The reproduction fails before the fix and passes after; blast radius checked; data repair named if stored data is wrong |
| `maintenance` | Dependency bump, refactor, tooling, docs | Behaviour does not change: existing tests stay green and unchanged unless an API they use changed deliberately |

Reuse what the caller did — branch, plan, failing test, approvals; do not re-investigate a supported diagnosis or redesign an approved plan.

**Search before you write.** For each component, query, helper, validator, error code or adapter you are about to add, search for an existing one and reuse or extend it. Business rules you cannot find in the issue, spec or code are asked, never assumed.

**Gate by tier:**
- Quick: the intent is one clear sentence.
- Standard: the plan has the inline design check (placement, reuse, next feature, tests — `work-context` §2a). An answer that needs new structure makes the task Structural.
- Structural / High-risk: the `design-review` is done before production code (a bug's reproduction test may come first), and the build follows its decisions.

## 2. Build

Work on a branch, never the default branch. New behaviour follows `tdd`; tests follow `testing-doctrine` (quality plugin). Config, docs, generated code and pure refactors use their own checks instead of a manufactured red test.

Use the area skill for each part you touch, and only those: the routing table is in [references/routing.md](references/routing.md). Find **companions** before editing and change the source, never the generated output: contract → generated clients; bridge definitions → generated platform code; string resources → accessors; entities → migration; new configuration → the example config; docs describing the changed behaviour.

Keep to scope. Something else broken → `file-bug`, not a drive-by fix. Code that breaks a convention is never copied. A failing step is evidence: diagnose it, then fix or revert that increment deliberately. For refactors follow [references/refactoring.md](references/refactoring.md).

## 3. Verify the actual change

Choose evidence by what changed:

| Change | Evidence required |
|---|---|
| Domain / server behaviour | Unit + integration tests through the real entry point; build with warnings as errors |
| API / auth | Integration tests for allowed **and** forbidden callers; regenerated client compiles; contract drift check green |
| Data / migration | Applied to a local database; generated SQL read (`add-migration`); data checks (`data-check`) |
| UI | One test per changed state; screenshots of changed states with synthetic data compared with the design |
| Platform / background / widgets | Builds for every platform; `device-test` rows on real devices when timing or OS behaviour changed |
| Safety-critical (the project's list) | A test per failure mode in `testing-doctrine` proving the critical action still happens or the failure is surfaced |
| Personal data, auth, sharing, uploads | `security-privacy-review`; forbidden-caller and removed-member tests |
| Performance-sensitive | `perf-check` against the budget |
| Maintenance | The suites and lint of every affected area; all platform builds for a native dependency bump |
| Quick (copy, style, docs, config) | The check that would catch a mistake in that file: build, lint, a screenshot, a link check |

While iterating run only the tests for what changed. Run each required full suite **once on the final candidate**, and again only if its inputs change. Record each check as **command → result**. A missing device, credential or SDK is blocked verification, never a pass.

**Gate:** each acceptance criterion has evidence and the checks the tier and project require pass.

## 4. Review and hand off

1. `pre-commit`; small conventional commits.
2. Review at the tier's depth (`work-context` §2): Quick → self-review of the diff with the `code-review` short checklist; Standard → one independent `code-review` at the end, the reviewer briefed with the task card, the diff and the agent brief; Structural / High-risk → independent review with a full design pass, plus `security-privacy-review` when personal data, auth, sharing, uploads, payments or analytics are touched. Fix findings in one batch; re-review only the delta; two rounds at most.
3. `create-pr`, `ci`, `deploy-check` when the change can break users after merge, then `merge` under the project's policy.

Report: what was implemented against the criteria; files by area; decisions; **checks with their actual output**; limitations and what was not verified; debt found, each with an issue. Keep implemented, verified, PR open, CI green, merged and released distinct.

## Rules

- New behaviour needs a test that fails without it; never weaken or delete a test to make a change pass.
- Never swallow an error on a safety-critical path; never silently lose data or broaden permissions to finish.
- No speculative abstractions and no unrelated cleanup.
- An external write (push, comment, deploy) needs authorization for that destination; reuse what was already given.

## Composition

| From | This skill | To |
|---|---|---|
| `work-context`, `start-issue`, `new-feature`, `bugfix` | Built, verified change with evidence | `pre-commit` → `create-pr` → `code-review` at the tier's depth → `ci` → `deploy-check` → `merge` |
