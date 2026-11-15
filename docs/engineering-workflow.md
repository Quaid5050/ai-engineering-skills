# Engineering workflow

One skill per step. Each skill reads the target project's own rules first and adapts to them. When a step has a skill, use it — do not improvise the step.

## The lifecycle

```
idea ──► shape-idea ──► bootstrap-project
                        (repo + main, protection, tracker, bootstrap issue, stack decisions,
                         walking skeleton, AGENTS.md, conventions + architecture tests, CI)
        │
        ▼
feature:  investigate-feature (docs issue) ──► spec ──► design-review (spec level, on the epic)
          ──► feature-to-issues (epic + slices) ──► docs PR merged
          small feature: investigate-feature ──► file-feature ──► docs PR
bug:      file-bug ──► investigate-bug (reproduction test) ──► bugfix
        │
        ▼
 start-issue ──► design-review (slice level, on the slice issue, BEFORE production code)
        │
        ▼
 implement (feature | bug | maintenance)
   ├─ engineering-principles + backend-, mobile-, web-conventions, shared-core
   ├─ tdd + testing-doctrine + write-tests
   ├─ add-endpoint, add-migration, add-scheduled-job, add-file-upload,
   │  design-to-screen, build-web-screen, add-web-page,
   │  background-work, offline-queue, home-widget, analytics-event
   └─ perf-check, accessibility-audit, security-privacy-review (when touched)
        │
        ▼
 pre-commit ──► create-pr ──► code-review (reviewer agent posts it: dimensions + design pass)
        │
        ▼
 ci ──► deploy-check (verdict posted) ──► device-test (mobile; before merge by default —
        │                                  or listed open and batched before release if AGENTS.md says so)
        ▼
 merge (eight gates; the merging session reads the diff)
        │
        ▼
 release (per component: backend deploy | web deploy | over-the-air patch | store release) ──► observe
        │
        ▼
 cleanup        incident (tracking issue) ──► postmortem ──► capture-lesson ──► create-skill
```

## Which skill when

| You want to… | Skill | Plugin |
|---|---|---|
| Turn an idea into a brief and an MVP plan | `shape-idea` | lifecycle |
| Make a repository agent-ready | `bootstrap-project` | lifecycle |
| Build one feature end to end | `new-feature` | lifecycle |
| Understand a feature before building it | `investigate-feature` | lifecycle |
| Write the plan for a non-trivial feature | `spec` | lifecycle |
| Turn a spec into an epic with sub-issues | `feature-to-issues` | lifecycle |
| File one scoped feature / a bug (bugs: file-bug → investigate-bug → bugfix) | `file-feature` / `file-bug` | lifecycle |
| Pick up an issue | `start-issue` | lifecycle |
| Review a plan before code | `design-review` (+ `architect` agent) | lifecycle (+ agents) |
| Build and verify an approved change | `implement` | lifecycle |
| Find a root cause / fix a bug | `investigate-bug` / `bugfix` | lifecycle |
| Decide where code goes, which pattern fits | `engineering-principles` | lifecycle |
| Check before committing | `pre-commit` | lifecycle |
| Open a PR | `create-pr` | lifecycle |
| Get CI green / debug CI | `ci` | lifecycle |
| Check what breaks users after deploy | `deploy-check` | lifecycle |
| Merge | `merge` | lifecycle |
| Ship to users / watch production | `release` / `observe` | lifecycle |
| Handle a live problem / write it up | `incident` / `postmortem` | lifecycle |
| Tidy up after merge | `cleanup` | lifecycle |
| Test rules / test-first loop / write tests | `testing-doctrine` / `tdd` / `write-tests` | quality |
| Review a diff | `code-review` (+ `reviewer` agent) | quality (+ agents) |
| Review security and privacy | `security-privacy-review` | quality |
| Check accessibility / performance | `accessibility-audit` / `perf-check` | quality |
| Add a product analytics event | `analytics-event` | quality |
| Structure server code / add an endpoint / change the schema / query data | `backend-conventions` / `add-endpoint` / `add-migration` / `data-check` | backend |
| Add a scheduled or background server job, or outbound notifications | `add-scheduled-job` | backend |
| Accept file uploads or attachments on the server | `add-file-upload` | backend |
| Structure an app / share a core / background work / offline queue | `mobile-conventions` / `shared-core` / `background-work` / `offline-queue` | mobile |
| Build a screen from a design / a widget / test on devices | `design-to-screen` / `home-widget` / `device-test` | mobile |
| Structure a web front end (content site or web app) | `web-conventions` | web |
| Build a web app screen (forms, data, auth, errors, states) | `build-web-screen` | web |
| Add a content page or section | `add-web-page` | web |
| Fill test gaps in existing code | `tester` agent | agents |
| Create or update a skill / record a decision / encode a lesson | `create-skill` / `decision` / `capture-lesson` | meta |

## Shared rules (every skill inherits these)

- **The project wins.** Its `AGENTS.md`, `CLAUDE.md` and conventions override any skill on facts (commands, paths, names) and policy (who merges, attribution, labels). A skill that disagrees with the code on a fact says which line is stale. The project's safety-critical list and optional policies (PR CI off, batched device tests, whether the agent merges) are read from `AGENTS.md`; skills' examples are only examples.
- **No work without an issue**; work on a branch created from it; the PR closes it.
- **Tests first.** A behaviour change without a test that failed first is not done.
- **Design review before production code** for every feature and non-trivial fix (spec level on the epic, slice level on the slice issue; a reproduction test may come first); **a design pass** in every code review, posted by the reviewer agent.
- **Lessons are encoded, not remembered:** in a consumer project, in its own `AGENTS.md`, conventions, tests and skills (never in the installed plugin files), with an upstream issue for general lessons; in this repository, in the skills themselves.
- **The speed rule:** speed may reduce test reruns and review rounds, never the tests written, the design review or the design pass.
- **Safety-critical paths** (a silent failure harms a person or loses money or data) get failure-path tests, never swallow errors, and their PR explains the failure mode.
- **Personal data** is never logged at shipped levels, sent to third-party analytics, or pasted into issues, PRs, commits or test names.
- **Outward-facing actions** (issues, labels, comments, pushes, PRs, releases, messages) need the owner's go-ahead unless the request already gave it. Required review comments on the project's own PRs and issues are part of the work.
- **Report states precisely:** implemented, verified, PR open, CI green, merged, released.
- **The author never reviews its own work** as the independent review: the `architect` and `reviewer` agents run with a fresh context.
