---
name: implement
description: "The shared build-and-verify contract for any approved change — feature, bug fix or maintenance: check the issue gate and the posted design review, search before writing, build test-first with the area skills and their companions (contract and generated clients, migrations, strings, bridges, docs), refactor safely (pin behaviour, move then change, always green), verify by change type with real command output, never call missing devices or credentials a pass, then pre-commit, PR, independent review posted on it, CI, deploy check and merge. Trigger on /implement, 'implement this', 'build this approved change', 'make the change and verify it', 'refactor this', 'upgrade this dependency', 'clean up this code'."
argument-hint: "[issue number, spec slice, investigation report, or scoped request]"
license: MIT
metadata:
  version: "1.0.0"
---

# Implement

Build `$ARGUMENTS` (an issue, a spec slice, an investigation report, or a scoped request) and prove it works. `new-feature`, `bugfix` and `start-issue` hand off here; this skill does not call them back. If no change is described, ask for it.

## 0. Read the project

- `AGENTS.md`: commands for build, lint and tests per area; which local checks CI does not run; the definition of done.
- The conventions for every area you will touch: `engineering-principles` and the stack skill (`backend-conventions`, `mobile-conventions`, `shared-core`, `web-conventions`), plus the project's own conventions doc and placement table. Read them **before** writing code.

## 1. Establish the handoff

**Issue gate:** there is an issue for this change (docs and chores included), in its milestone, with a branch linked to it. None → stop and create it (`file-feature`, `file-bug`, `feature-to-issues`), then `start-issue`. Never build first and file the issue afterwards.

Pick the mode:

| Mode | Input | Extra obligations |
|---|---|---|
| `feature` | Issue with acceptance criteria | Every criterion gets a test; every designed state is built; scope follows "Out of scope" |
| `bug` | Investigation with root cause + failing test | The reproduction fails on the code before the fix and passes after; blast radius checked; data repair named if stored data is wrong |
| `maintenance` | Dependency bump, refactor, tooling, docs | Behaviour does not change: existing tests stay green **unchanged**; no invented criteria; architecture baselines stay empty |

Reuse what the caller did (branch, plan, failing test, approvals); do not re-investigate a supported diagnosis or redesign an approved spec.

**Search before you write.** For each piece you are about to add — a component, a query, a helper, a validator, an error code, an adapter — search for an existing one and reuse or extend it. A second implementation of the same thing is a review finding. Business rules you cannot find in the issue, spec or code are asked, never assumed.

**Gate:** behaviour, areas, verification method and scope are concrete, and — for a feature slice or non-trivial fix — the issue has the posted `## Design review` (`design-review`) before any production code (a bug's reproduction test may already be committed); the build follows its decisions. An open product decision → ask, and work on the independent parts meanwhile.

## 2. Build

On the issue branch, never `main`. Behaviour changes follow `tdd` and `testing-doctrine` (quality plugin); the commands are in `write-tests` and `AGENTS.md`.

Use the area skill for each part:

| Part | Skill |
|---|---|
| Endpoint / contract | `add-endpoint` (backend plugin) |
| Schema | `add-migration` (backend plugin) |
| Scheduled or background server job, outbound notifications | `add-scheduled-job` (backend plugin) |
| File uploads and attachments (server side) | `add-file-upload` (backend plugin) + `security-privacy-review` (quality plugin) |
| Mobile screen from a design | `design-to-screen` (mobile plugin) |
| Web app screen (forms, data, auth) | `build-web-screen` (web plugin) |
| Web content page or section | `add-web-page` (web plugin) |
| Rules shared by Android and iOS | `shared-core` (mobile plugin) |
| Mobile background work, offline queue | `background-work`, `offline-queue` (mobile plugin) |
| Widget / live activity / tile | `home-widget` (mobile plugin) |
| Personal data, auth, sharing, uploads | `security-privacy-review` (quality plugin) |
| Product event | `analytics-event` (quality plugin) |

**Companions** — find them before editing; change the source, never the generated output: contract file → generated clients; bridge definitions → generated platform code; string resources → generated accessors; entities → migration; new configuration → the example config file; docs that describe the changed behaviour.

Keep to the issue's scope. Something else broken → `file-bug`, not a drive-by fix. Code you meet that breaks a convention → file it (or fix it in its own PR); never copy it.

### Refactoring safely (maintenance mode)

1. **Pin the behaviour first.** Missing coverage → characterisation tests on the old code, passing, committed alone.
2. **Move, then change** — separate commits, tests green after each.
3. **Small steps, always green.** A red step is reverted, not debugged forward.
4. **The contract does not move** unless the slice says so.
5. **Baselines stay empty.** A new rule lands with the code fixed; if impossible, a shrinking-only baseline with a reason per entry and an issue to empty it.

## 3. Verify the actual change

Choose checks by what changed:

| Change | Evidence required |
|---|---|
| Domain / server behaviour | Unit + integration tests through the real entry point; build with warnings as errors |
| API / auth | Integration tests for allowed **and** forbidden callers; regenerated client compiles; contract drift test green |
| Data / migration | Applied to a local database; generated SQL read (`add-migration`); data checks (`data-check`) |
| UI | One test per state; screenshots of each changed state with synthetic data, compared with the design |
| Platform / background / widgets | Builds for every platform; `device-test` rows on real devices; battery reading when background behaviour changed |
| Safety-critical (the project's list in `AGENTS.md`) | A test per failure mode in `testing-doctrine`, proving the critical action still happens or the failure is surfaced |
| Privacy | `security-privacy-review` checks; forbidden-caller and removed-member tests |
| Performance-sensitive | `perf-check` against the budget |
| Maintenance | The full suites and lint for every affected area; all platform builds for a native dependency bump |

Record each check as **command → result**. A missing device, emulator, credential or SDK is **blocked verification, never a pass**: say exactly what remains.

**Gate:** each acceptance criterion has evidence and the required checks pass.

## 4. Review and hand off

1. `pre-commit`; small conventional commits.
2. `create-pr` — it opens the PR and then has the `reviewer` agent (agents plugin) run `code-review` (quality plugin) with fresh context and **post** it on the PR; the author never reviews its own work independently. `security-privacy-review` runs for personal data, auth, sharing or uploads.
3. `ci`, `deploy-check`, then `merge`.

Final report (and the basis of the PR body):
- **What was implemented**, against the acceptance criteria.
- **Files changed**, grouped by area.
- **Decisions** taken (decision records for costly ones).
- **Checks run, with their actual output** — never "tests pass" without having run them; anything not run says why.
- **Known limitations** and anything not verified.
- **Technical debt** added or found, each with an issue.

Keep **implemented**, **verified**, **PR open**, **CI green**, **merged**, **released** distinct — never round one up to the next.

## Rules

- No code without a red test asking for it (except config, docs and generated code, which use their own checks).
- Never weaken or delete a test to make the change pass.
- Never swallow an error on a safety-critical path.

## Composition

| From | This skill | To |
|---|---|---|
| `start-issue`, `new-feature`, `bugfix` | Built, verified change with evidence | `pre-commit` → `create-pr` → `code-review` (posted) → `ci` → `deploy-check` → `merge` |
