# Changelog

Every plugin is versioned on its own ([semantic versioning](https://semver.org/), rules in [CONTRIBUTING.md](CONTRIBUTING.md)). Newest first.

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
