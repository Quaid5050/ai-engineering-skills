# Changelog

## Marketplace 2.0.0 — 2026-11-27
Risk-based workflow, audit remediation and scoped capability expansion. Breaking workflow/gate changes use major versions; skill names and existing paths remain stable. See docs/remediation.md for implementation and evidence limits.

**Fast by default, strict where it matters** (issue #5, on top of the audit remediation):
- `work-context` (foundation) picks Quick, Standard or Structural/High-risk once per task with concrete triggers and says exactly which steps, reviews, subagents and test runs each tier gets. A design review and the architect run only when a change creates structure (feature or module from scratch, layer/service, data model, contract, dependency, cross-cutting refactor) or touches a declared high-risk area; Standard work answers placement, reuse and tests inline in its plan.
- Read once, brief others: a task card replaces re-deriving facts; subagents get a brief and the project's `docs/agent-brief.md` (new `bootstrap-project` template) instead of whole skills; agents preload only the skill they run (`skills:`).
- Re-reviews cover only `git diff <reviewed>..HEAD`; findings are batched; two rounds at most; full suites run once on the final head.
- `scripts/check.py` caps a SKILL.md body at 3,000 words and an agent prompt at 600 words, and checks agents' preloaded skills exist.
- Restored as references the concrete content the remediation had deleted: implement's area routing, evidence table and refactor recipe; merge's gate table, commands, stacked PRs and the speed rule; design-review's template; code-review's output template and delta re-review; testing-doctrine's failure-paths-first, fake-boundary table, rungs ladder, test types and reject-on-sight; notification port, idempotency example, Postgres migration rules, backend default profile, the emitted-script check for static sites.
- Fixed: the commit guard no longer blocks ordinary commands (conventional-commit and heredoc messages, `grep commit`), allows detached HEAD, scans only staged additions in one call, names the file and line, and fails open with a warning without `python3`; the `READPAST` statement; reviewer, architect and tester have read-only `Bash` again; broken references (`merge` gate 8, testing-doctrine sections); headings and identical Composition tables of the 18 new skills, now marked draft.

## agents 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## ai 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## architecture 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## backend 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## data 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## desktop 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## foundation 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## guardrails 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## lifecycle 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## meta 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## mobile 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## operations 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## quality 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## security 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## specialist 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## systems 1.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

## web 2.0.0 — 2026-11-27
- Add or revise scoped procedures, dependencies and validation. Historical audit evidence remains pinned to its original commit.

Every plugin is versioned on its own ([semantic versioning](https://semver.org/), rules in [CONTRIBUTING.md](CONTRIBUTING.md)). Newest first.

## quality 1.2.0 — 2026-11-27
- New `static-catalogs`: a closed set the app defines (languages, plans, providers, modes) becomes one row per case instead of one switch per attribute; a decision table for when a data file plus code generation is justified (shared across apps, or an outside spec) and when it is not; characterisation tests over every case and attribute before the move, frozen persisted ids, guards. References: Swift, TypeScript. Before this, no skill said when configuration-plus-codegen is the right call, so an app-owned enum could be moved to a config file and a generator for no gain.

## quality 1.1.0 — 2026-11-26
- `testing-doctrine` §9: the test types (unit, integration, end-to-end, smoke, regression, device) with what each proves, its size and when it runs; smallest type that catches it, keep the pyramid, a regression test per bug fix, smoke first, coverage as a signal. Before this, smoke, regression and end-to-end were named only in passing in other skills.

## lifecycle 1.0.0 — 2026-11-15
- First public release: `shape-idea`, `bootstrap-project`, `investigate-feature`, `spec`, `feature-to-issues`, `file-feature`, `file-bug`, `start-issue`, `design-review`, `new-feature`, `implement`, `investigate-bug`, `bugfix`, `pre-commit`, `create-pr`, `ci`, `deploy-check`, `merge`, `release`, `observe`, `incident`, `postmortem`, `cleanup`, `engineering-principles`.
- Encodes the initial lessons L1–L6 in [docs/lessons.md](docs/lessons.md): design review before code, placement rows, allowlist architecture tests, the merging session reads the diff, the speed rule, hosted runners for public repositories.
- Hardened by two fresh-agent dry runs of the whole lifecycle (Django + React web; Spring/Kotlin + Flutter mobile): one order everywhere, eight merge gates (design review before production code; deploy-check and security/privacy verdicts posted), spec-level and slice-level design reviews, docs issue before the epic, bootstrap order (repo → protection → tracker → issue → PR), consumer projects never edit installed plugin files.

## quality 1.0.0 — 2026-11-15
- First public release: `testing-doctrine`, `tdd`, `write-tests`, `code-review` (with the separate design pass), `security-privacy-review`, `accessibility-audit`, `perf-check`, `analytics-event`.

## backend 1.0.0 — 2026-11-15
- First public release: `backend-conventions` (references: .NET, Django, Node, Spring), `add-endpoint`, `add-migration`, `add-scheduled-job`, `add-file-upload`, `data-check`.

## mobile 1.0.0 — 2026-11-15
- First public release: `mobile-conventions` (references: Flutter, React Native, Kotlin, Swift), `shared-core` (Kotlin Multiplatform reference), `background-work`, `offline-queue`, `design-to-screen`, `home-widget`, `device-test`.

## web 1.0.0 — 2026-11-15
- First public release: `web-conventions` (content sites and web apps; references: React/Next.js, Astro), `build-web-screen`, `add-web-page`.

## agents 1.0.0 — 2026-11-15
- First public release: `architect`, `reviewer`, `tester`.

## meta 1.0.0 — 2026-11-15
- First public release: `create-skill`, `decision`, `capture-lesson`.

## guardrails 1.0.0 — 2026-11-15
- First public release: secret scan before commits, no commits on the main branch.
