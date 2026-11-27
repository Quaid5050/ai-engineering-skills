---
name: code-review
description: "Review a diff or PR on any stack at the depth its risk tier needs — Quick changes get a short checklist, Standard changes one independent review of the diff, Structural/High-risk changes every dimension plus a full design pass. Dimensions: safety-critical paths, privacy and tenant isolation, tests you can trust, correctness, contract, data, platform and battery, design and UX, performance, observability, simplicity, layer placement, conventions, repo hygiene. Each finding has severity, file:line, failure scenario, fix and the rung where it should have been caught; plus a merge risk tier. Re-reviews cover only the fix delta. Use before merge. Trigger on /code-review, 'review this', 'review the PR', 'review my changes', 'check the diff', 'is this ready to merge'."
argument-hint: "[PR number, branch, path, or empty for the current branch]"
license: MIT
metadata:
  version: "2.0.0"
---

# Code review

Review `$ARGUMENTS`: a PR number, a branch, a path, or empty for the current branch against the main branch.

```bash
git diff origin/main...HEAD                     # current branch (use the project's main branch name)
gh pr diff <number>                             # a PR (or the tracker's equivalent)
gh pr view <number> --json title,body,files,labels
git diff <reviewed-sha>..HEAD                   # re-review: only what changed since the last review
```

## 0. Read the project

Reuse the task card and tier from `work-context` (foundation plugin). Read the project's agent rules (merge gates, review format, safety-critical list, attribution rules) and the agent brief. Read the linked issue and, for Structural work, its design review. Read **only** the conventions checklists for areas the diff touches; what this session already read is not re-read. Review the diff, not the whole codebase: files the diff does not change are context, not review targets.

## 1. Depth by tier

| Tier | Who | What |
|---|---|---|
| **Quick** | The author, as a labelled self-review | The short checklist below. No design pass. |
| **Standard** | One independent reviewer (the `reviewer` agent, agents plugin), briefed with the task card, the diff and the agent brief | Dimensions 1–3 always; others the diff touches; the design pass for **new** files and moved code only |
| **Structural / High-risk** | Independent reviewer; `security-privacy-review` too when dimension 2 hits | Every applicable dimension and the full design pass against the design review |

The project's rules can require more (for example an independent review of every change); follow them. Never call a self-review independent.

**Short checklist (Quick):** the diff does only what the task says · nothing on a safety, auth, data or contract path changed (if it did, the task is not Quick — re-classify) · builds, lints and the targeted check pass · no secret, debug code or forbidden attribution · user-facing text uses the project's localisation and tokens · docs match the change.

## 2. Shape first

Is this one logical change? Behaviour change and refactor mixed (ask to split)? Does it do what its issue says and nothing more? Is it small enough to review well (~400 hand-written lines is a good limit)?

## 3. Dimensions

The first three outrank the rest.

| # | Dimension | Look for |
|---|---|---|
| 1 | **Safety-critical paths** | Anything where a silent failure harms a person or loses money or data: can the effect be lost, delayed, duplicated or reach the wrong person? Every catch logs and surfaces; retries bounded with a fallback; timers on the injected clock; idempotency keys; failure-path tests exist, including "dedupe does not swallow real events" (`testing-doctrine`). |
| 2 | **Privacy & isolation** | Every resource endpoint checks ownership/membership; queries filter by tenant; the logging rule in `security-privacy-review`; sharing opt-in and visible. Any hit → `security-privacy-review`. |
| 3 | **Tests you can trust** | Tests follow `testing-doctrine`: independent oracles, behaviour not implementation, proven able to fail. Examples, properties and sequence tests are all valid. New behaviour without a test that fails without it is `major`. |
| 4 | Correctness | UTC and time zones, null/empty, first item missing, out-of-order events, offline and resume, races, pagination edges. |
| 5 | Contract | Contract file changed with the API; generated clients regenerated, never hand-edited; breaking changes versioned; stable error codes. |
| 6 | Data | Engine-specific locks and rewrites assessed, expand → migrate → contract, constraints match domain limits (`add-migration`). |
| 7 | Platform & battery | Background work justified and measured; OS limits handled; permission asked after explanation (`background-work`). |
| 8 | Design & UX | Design tokens, no hard-coded colours or strings, localisation, every designed state built, accessibility labels, reduced motion. |
| 9 | Performance | Any DB, cache or HTTP call in a loop; unbounded queries; missing indexes; I/O under a lock; work on the UI thread. A hot-path change without a measurement is `major` (`perf-check`). |
| 10 | Observability | New failure modes produce an event or metric someone sees; logs have context but no personal data. |
| 11 | Simplicity | Less code wins; one owner per rule; no dead code; names say what things are (`engineering-principles` checklist). |
| 12 | Layer placement | New types pass the concept test against the chosen architecture; inline shape validation in a handler is `minor`. |
| 13 | Conventions | The checklist of each stack skill the diff touches; rate by impact, house style alone is not major. An existing violation the diff touches gets an issue. |
| 14 | Repo hygiene | Conventional commits, the project's attribution rules, no secrets, generated files in sync, docs updated. |
| 15 | Required evidence | Security and deploy-readiness evidence the tier requires exists before merge; during an early review, list it as pending. |

## 3a. Design pass

Review the diff once more for design only — is the code in the right place, and will it be copied wrongly? Standard: new files and moved code only. Structural / High-risk: everything, against the posted design review.

1. **Placement:** each new or moved file is in its placement row for its kind.
2. **Duplication across features:** does the diff add something another feature already has? **Search** for it; do not guess.
3. **Reuse:** existing generic pieces are used instead of rewritten.
4. **Responsibility boundaries:** accidental infrastructure coupling isolated, judged against the project's architecture.
5. **Validation, secrets, storage homes:** shape checks in the validation unit; each secret its own configuration; files behind the storage port.
6. **Design evidence (Structural only):** the design review exists for this revision and the code follows it.

Report each check you ran with what was searched. A missing design review blocks only when the tier or the project requires one.

## 4. Each finding

- **Severity:** `critical` (an effect can silently fail on a safety path, personal data exposed, data loss, crash on a core path) · `major` (wrong behaviour, missing test for new behaviour, contract drift, design the next feature would copy) · `minor` · `nit`.
- **Where:** `file:line`. **Scenario:** concrete inputs → wrong outcome. **Fix:** concrete change.
- **Rung:** where it is caught today and the earliest rung that should catch it: type → lint → architecture test → unit/integration test → CI → design review → code review → device test → alert → user report.

Unprovable structural worries go in a separate, non-blocking **Suspicions** list.

## 5. Merge risk and output

Give a risk tier separate from the verdict: **low** (isolated, tested, easy to revert), **medium** (shared code, migrations, platform code), **high** (safety-critical, privacy boundary, large-table migration, release-only fix). Use the template in [references/output.md](references/output.md).

## 6. Publish and re-review

Post the review as **one** PR comment written to a file first, checked against the project's attribution rules (`gh pr comment <number> --body-file <file>`). On the project's own PR this is part of the required review; on someone else's, ask first.

**Re-review covers the delta.** After fixes, review `git diff <reviewed-sha>..HEAD` against the open findings plus any interaction with code those fixes touch — not the whole PR again. If the host can resume the same reviewer, resume it instead of starting a cold one. Post `## Code review — <new SHA> (re-review)` listing fixed and remaining findings. Two rounds at most; a third means re-plan. A PR is ready when the latest review covers the head (or everything after it is a reviewed fix) and no `critical`/`major` is open.

## Dependency-update PRs

Same gate, lighter dimensions: release notes between the versions, the lock-file diff for unexpected transitive bumps and install scripts, the area's checks run, and `deploy-check` for major versions and native dependencies. A patch bump with green checks is Quick.

## Rules

- Review the code, not the author; every finding has a scenario.
- Never approve a safety-critical change without failure-path tests.
- "No issues" only after every dimension the tier requires was checked — list them.
- Do not re-review unchanged, already-reviewed code, and do not raise the review depth beyond the tier without a concrete reason.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `bugfix`, `create-pr` (lifecycle), the `reviewer` agent | Findings at the tier's depth, posted on the PR | `security-privacy-review` when dimension 2 hits; `merge` checks the latest review covers the head |
