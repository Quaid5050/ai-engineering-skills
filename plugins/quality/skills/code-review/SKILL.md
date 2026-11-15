---
name: code-review
description: "Review a diff or PR on any stack — shape first, then every applicable dimension (safety-critical paths, privacy and tenant isolation, tests you can trust, correctness, contract, data, platform and battery, design and UX, performance, observability, simplicity, layer placement, conventions, repo hygiene), then a separate mandatory design pass (placement, duplication across features, reuse, technical code out of business layers, validation/secret/storage homes, design review posted before code). Each finding has severity, file:line, failure scenario, fix and the rung where it should have been caught; plus a merge risk tier. Use before every merge. Trigger on /code-review, 'review this', 'review the PR', 'review my changes', 'check the diff', 'is this ready to merge'."
argument-hint: "[PR number, branch, path, or empty for the current branch]"
license: MIT
metadata:
  version: "1.0.0"
---

# Code review

Review `$ARGUMENTS`: a PR number, a branch, a path, or empty for the current branch against the main branch.

```bash
git diff origin/main...HEAD                     # current branch (use the project's main branch name)
gh pr diff <number>                             # a PR (or the tracker's equivalent)
gh pr view <number> --json title,body,files,labels
```

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`: merge gates, review format, what counts as safety-critical, commit and attribution rules.
2. Read the linked issue or spec and its posted design review (`design-review`, lifecycle plugin), so you review against intent, not only the code.
3. Read the conventions for every area the diff touches: `engineering-principles` (lifecycle plugin) and the stack skills (`backend-conventions`, `mobile-conventions`, `web-conventions`) or the project's own conventions docs.

**Every change gets this review before merge** — features, fixes, docs, CI and dependency updates. For a PR, run it through the `reviewer` agent (agents plugin) with a fresh context, so the review is independent of the session that wrote the code.

## 1. Shape first

Before line comments: is this one logical change? Behaviour change and refactor mixed (ask to split)? Does it do what its issue says and nothing more? Is it small enough to review (> ~400 changed lines of hand-written code → suggest splitting)?

## 2. Dimensions

Go through every dimension the diff can touch. The first three outrank the rest.

| # | Dimension | Look for |
|---|---|---|
| 1 | **Safety-critical paths** | Anything where a silent failure harms a person or loses money or data: can the effect be lost, delayed, duplicated or reach the wrong person? Every catch logs and surfaces; retries bounded with a fallback; timers on the injected clock; idempotency keys; failure-path tests exist, including the paired "dedupe does not swallow real events" tests (`testing-doctrine`). |
| 2 | **Privacy & isolation** | Every resource endpoint checks ownership/membership with the project's status codes; queries filter by tenant; the logging rule in `security-privacy-review` §5; sharing is opt-in and visible. Any hit → run `security-privacy-review`. |
| 3 | **Tests you can trust** | Tests follow `testing-doctrine`: exact, hard-coded, no mocks of own code, behaviour not implementation, can fail. New behaviour without a red-first test is a finding. |
| 4 | Correctness | UTC and time zones, null/empty, first item missing, out-of-order events, offline and resume after hours, races between push and pull, pagination edges. |
| 5 | Contract | Contract file changed with the API; generated clients regenerated, never hand-edited; breaking changes versioned; stable error codes. |
| 6 | Data | Migrations safe on large tables (no rewrite, nullable/defaults, online indexes), expand → migrate → contract, constraints match domain limits (`add-migration`, backend plugin). |
| 7 | Platform & battery | Background work justified and measured; OS killers handled; permission asked after explanation; both platforms behave the same (`background-work`, mobile plugin). |
| 8 | Design & UX | Design tokens, no hard-coded colours or strings, localisation, every designed state built, accessibility labels, reduced motion (`accessibility-audit` for UI-heavy changes). |
| 9 | Performance | N+1 (any DB, cache or HTTP call in a loop), unbounded or in-memory-filtered queries, missing indexes, I/O while holding a lock, rebuild storms, work on the UI thread, payload size. A hot-path change without a measurement is `major` (`perf-check`). |
| 10 | Observability | New failure modes produce an error event or metric someone will see; logs have context but no personal data; analytics events from the catalogue (`analytics-event`). |
| 11 | Simplicity & changeability | Less code wins; one owner per rule; no second place to update; no dead code; names say what things are. Run the review checklist of `engineering-principles` §4. |
| 12 | Layer placement | Every new domain type passes the concept test (a file format, encoding, parser or crypto helper in the domain is `major`); shape validation built inline in a handler instead of its validation unit is `minor`. |
| 13 | Conventions | The checklist of each stack conventions skill the diff touches. Business logic, queries or transactions in an edge is `major`; otherwise `minor`. An existing violation the diff touches is a finding too, with an issue to fix it — architecture baselines are empty, no exception by precedent. |
| 14 | Repo hygiene | Conventional commits by the project's author rules, no attribution the project forbids, no secrets, generated files in sync, docs updated with the behaviour. |
| 15 | Required verdicts | `merge` gate 8 (lifecycle plugin): when the diff changes the API, data, platform code, configuration or scheduling, a `deploy-check` verdict is posted; when it touches personal data, auth, sharing or uploads, a `security-privacy-review` is posted. Missing → `major`; an unsafe row or critical finding open without the owner's quoted acceptance → `critical`. |

## 2a. Design pass (separate, mandatory, never skipped for speed)

After the dimensions, review the diff **once more for design only** — not bugs, not safety, but whether the code is in the right place and will not be copied wrongly. Agents copy the code next to them: a wrong placement nobody stops becomes the next feature's template.

1. **Placement:** every new or moved file is in its placement row (`engineering-principles` §3 and the project's table) for its kind: business rule, port, adapter, secret, storage, file format, upload body, rate limit, loop, shared code, platform decision.
2. **Duplication across features:** does the diff add something another feature already has or will need — a per-feature storage class, a second upload reader, a second copy of a rule, a feature-specific variant of a generic port? **Search for it** (`grep`), don't guess.
3. **Reuse:** does it use the existing generic pieces (storage port, upload reader, wire-enum mapping, access-check unit, shared module, shared core rules) instead of rewriting them?
4. **Technical code out of business layers:** no file format, encoding, parsing, crypto, vendor type or protocol detail in the domain, use-case rules or the shared core.
5. **Validation, secrets and storage homes:** shape checks in the validation unit; each secret its own validated configuration; files only behind the storage port.
6. **The design review:** a feature or non-trivial fix has a design review posted on its issue **before** the first code commit, and the diff follows its decisions (or says why not). Missing → `major`.

**Severity:** a design finding is `major` when the next feature would copy it (a pattern, a per-feature duplicate of a generic piece, technical code in a business layer, a missing design review); otherwise `minor`. A design-pass `major` blocks the merge like any other.

**Gate:** all six checks are reported, each with what was searched.

## 3. For each finding

- **Severity:** `critical` (an effect can silently fail on a safety path, personal data exposed, data loss, crash on a core path) · `major` (wrong behaviour, missing test for new behaviour, contract drift, design copied by the next feature) · `minor` · `nit`.
- **Where:** `file:line`.
- **Failure scenario:** concrete inputs → wrong outcome.
- **Fix:** concrete change.
- **Rung:** where it is caught today and the earliest rung where it should be, on the one ladder in `testing-doctrine` §8 (type → lint → architecture test → unit/integration test → CI → design review → code review → device test → alert → user report). Moving a class of bug earlier beats fixing one instance.

Structural worries you cannot prove go in a separate **Suspicions** list — named, non-blocking.

## 4. Merge risk

Always give a tier, separate from the verdict: **low** (isolated, tested, easy to revert), **medium** (shared code, migrations, platform code, anything uncertain), **high** (safety-critical path, privacy boundary, data migration on large tables, release-only fix).

## 5. Output

```markdown
## Code review — <short head SHA>
**Verdict:** approve | approve with fixes | changes required
**Risk tier:** low | medium | high — why

### Critical / Major / Minor / Nits
- [severity] file:line — problem. Scenario: … Fix: … Rung: test → type.

### Design pass
- [major|minor] file:line — placement / duplication / reuse / technical code / validation-secret-storage / design review. Who would copy it: … Fix: …
(or "No design findings", followed by the six checks and what was searched for each)

### Suspicions (non-blocking)
### Checked and fine
Every dimension checked with no findings, so "no issues" is a claim with coverage.
```

## 6. Publish on the PR

Post the review as **one** PR comment, written to a file first. Check the file against the project's attribution rules before posting (for example `grep -niE 'co-authored-by|generated with'`), then:

```bash
gh pr comment <number> --body-file <review-file>
```

Posting on the project's own PRs is part of the required review; on someone else's PR it needs the user's OK. After fixes: review **only the new commits** against the open findings and post `## Code review — <new SHA> (re-review)` saying which findings are fixed, which remain and why. A PR is ready only when the latest review covers the head commit (or everything after it is a reviewed fix), no `critical` or `major` is open, and the design pass has no open `major`.

## Dependency-update PRs

Same gate, lighter dimensions: read the release notes between the old and new versions for breaking changes, check the lock-file diff for unexpected transitive bumps and install scripts, confirm CI ran the jobs for the changed area (run them locally if CI skips that area), and apply `deploy-check` (lifecycle plugin) for major versions and native dependencies.

## Rules

- Review the code, not the author; findings need a scenario, not taste.
- Never approve a safety-critical change without failure-path tests.
- "No issues" only after every applicable dimension was checked — list them.
- The author never reviews their own work as the independent review; use the `reviewer` agent.
- The design pass (§2a) is never dropped or shortened, even when a brief asks for a quick review: trim test reruns and review rounds, not the design pass.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `bugfix`, `create-pr` (lifecycle plugin), the `reviewer` agent (agents plugin) | Dimensions + design pass + risk tier, posted on the PR | `security-privacy-review` when dimension 2 hits; `merge` (lifecycle) checks the posted review covers the head commit |
