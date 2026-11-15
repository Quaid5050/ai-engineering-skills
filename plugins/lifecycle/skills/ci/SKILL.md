---
name: ci
description: "Drive a pull request through continuous integration and debug failures — ship (watch the checks on the head commit to green, never re-run to get past a real failure), debug (find the first error, classify it, reproduce locally with the same command, fix the cause), optimize (measure the slowest steps over three runs), and change workflows safely (stable job names the merge gates refer to, pinned actions, no secrets in files, never a self-hosted runner on a public repository). Use when a PR is waiting on CI or CI is red. Trigger on /ci, 'watch CI', 'why is CI red', 'CI is failing', 'fix the build', 'is my PR green', 'speed up CI', 'add a workflow'."
argument-hint: "[ship PR | debug run-or-PR | optimize | workflow <change>]"
license: MIT
metadata:
  version: "1.0.0"
---

# CI

Handle `$ARGUMENTS`: `ship [PR]` (default), `debug [run|PR]`, `optimize`, or `workflow <change>`.

## 0. Read the project

1. Read the pipeline definition (`.github/workflows/*.yml` or the project's CI config) **before acting** — if it disagrees with this skill or with `AGENTS.md`, the file wins; say which line is stale.
2. From `AGENTS.md`: which checks the merge gates require (`merge`), which areas CI does **not** cover (those checks run locally and are pasted in the PR), the runner type, and where CI docs live.
3. Note path filters: a skipped job counts as passing only when its area did not change.

## 1. Ship

```bash
gh pr checks <PR> --watch --interval 30
gh pr view <PR> --json headRefOid,statusCheckRollup,mergeable,mergeStateStatus
```

- Confirm the checks belong to the PR's **current head commit** (a new push takes a moment to start a run).
- Red → `debug`. Green → check that the head is tested against current main: a PR that is behind (`mergeStateStatus: BEHIND`) or was just retargeted first merges main in, pushes, and gets a fresh green run.
- Green on a current head → `merge` decides the rest (review, design review, diff read).

**Gate:** every required check is green (or skipped because its area did not change) on the head commit, and the head contains current main.

## 2. Debug

```bash
gh run list --branch <branch> --limit 5
gh run view <run-id> --log-failed | tail -150
```

1. Find the **first** error in the log, not the last.
2. Classify it and reproduce it locally with the **same command** CI ran:

| Failure | Local reproduction |
|---|---|
| Build / compile (warnings as errors) | the CI build command, same configuration |
| Test | the single failing test by name, then its file |
| Lint / analyze / format | the same linter with the repo's config |
| Dependency resolution | compare lock files; a dependency bump often causes it |
| Environment (runner offline, service down, network, registry outage) | not reproducible; the log line shows it |
| Toolchain version | compare the pinned version with the local one; bump the pin on purpose, with the code |

3. Fix the **cause** in code, `pre-commit`, push to the PR branch, watch again.

**Re-run rule:** never re-run to get past a test, lint or build failure. Re-run only a clearly environmental failure, **once per commit**, quoting the log line that shows it is environmental. A test that fails sometimes is flaky: fix or delete it (`testing-doctrine`, quality plugin) — never re-run it green.

## 3. Optimize

Measure the slowest jobs and steps over **three runs** (`gh run view <id> --json jobs`), then try one change at a time and measure again: dependency caches keyed on lock files, path filters so docs-only changes skip builds, running independent jobs in parallel, splitting slow integration tests into their own job, test parallelism, cancelling superseded runs with `concurrency` — **only for pull requests**; on the main branch every commit's run completes, so a red main can be traced to its commit. Report before → after.

## 4. Workflow changes

- On a `ci/…` or `chore/ci-…` branch, through a PR like any change.
- Keep **job names stable** — the merge gates and branch protection refer to them. A rename updates both in the same PR.
- Pin third-party actions (major version at least; a commit SHA for anything with write access). Least-privilege `permissions:` per workflow.
- No secrets in workflow files; repository or environment secrets only, added with the user's OK. Never echo a secret.
- **Security rule: never attach a self-hosted runner to a public repository.** Anyone can open a PR from a fork and run code on it. Public repositories use hosted runners; a private repository that will become public removes its self-hosted runners first.
- Pull requests from forks get no secrets; workflows triggered by `pull_request_target` never check out and run the PR's code.
- Validate by pushing the branch and watching the run; run a manual dispatch for jobs that only run on main.

- A **PR links an issue** check, when the project uses the issue gate.
- Mobile clients: an iOS build needs a macOS runner; Android and most cross-platform analyse/test steps run on Linux.

A minimal template (issue-link job, toolchain examples, the concurrency rule) is in [references/github-actions.md](references/github-actions.md).

## Rules

- A red main is fixed before anything else merges.
- Never weaken a check (skip a test, lower a threshold, mark a job optional) to get green; that is a separate, reviewed decision.
- Pushing fix commits to the PR branch is part of the PR work; a force-push or pushing to someone else's branch needs the user's OK.

## Composition

| From | This skill | To |
|---|---|---|
| `create-pr`, `bugfix` | Checks green on the head commit | `deploy-check`, `merge` |
| A failing test | Debug | `investigate-bug` when the cause is not in the diff |

## Report

Each job → state → link; for failures: the first error, root cause, the fix commit, and the green run link.
