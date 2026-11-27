# Changelog

## Marketplace 2.0.0 — 2026-11-27
Risk-based workflow, audit remediation and scoped capability expansion. Breaking workflow/gate changes use major versions; skill names and existing paths remain stable. See docs/remediation.md for implementation and evidence limits.

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
