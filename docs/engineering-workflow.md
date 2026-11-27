# Engineering workflow

One skill per step, at the depth the task's **tier** needs. `work-context` (foundation plugin) picks the tier once per task; every other skill reads it. Each skill reads the target project's own rules first, and the project wins.

## Tiers: how much process a task gets

| Tier | Triggers | Route |
|---|---|---|
| **Quick** | Copy, styling, a UI tweak inside an existing component, docs, test-only, config/tooling, a patch-level bump, a one-line fix with a known cause — and no High-risk trigger | Read the touched code → change → targeted check → the touched area's suite once → self-review of the diff (`code-review` short checklist) → commit/PR. No subagents, no design review. |
| **Standard** | New or changed behaviour **inside existing structure**: a slice following an existing pattern, a bug fix in existing code, a new screen state or endpoint in an existing resource | 3–6 line plan with the **inline design check** (placement, reuse, next feature, tests) → `implement` test-first, targeted tests while working → required suites **once** on the final head → **one** independent review (reviewer agent with a brief) → fixes in one batch, delta re-review. |
| **Structural / High-risk** | A feature or module **from scratch**, a new layer/service/boundary, a data model or migration, a new resource or a breaking contract change, a new dependency, a cross-cutting refactor, or a project-declared high-risk area (auth, money, personal data, safety-critical, destructive data, delivery guarantees, background execution) | `investigate-feature` when unclear → `spec` → **`design-review` before code** (architect agent) → `implement` with failure paths first → independent review with a **full design pass** → `security-privacy-review` / `deploy-check` when touched → recovery plan. A High-risk fix with no new structure runs this in focused form: no spec; failure modes, tests and rollback only. |

Classify by what the change creates and what a mistake costs, not by line count: a one-line permission change is High-risk, a mechanical rename is Quick. Already-reviewed code the diff does not restructure is not design-reviewed again. A slice that follows a reviewed design is Standard.

## Why it is fast: read once, brief subagents, review the delta

- **Read once.** A skill or reference already read in the session is not re-read unless it changed or the context was compacted. Skills keep their procedure in `SKILL.md` and load `references/` only for the step that needs them (CI enforces body size limits).
- **Brief, don't re-teach.** A subagent starts with no memory of the conversation. It gets the task card, the diff or plan, and the project's **agent brief** (`docs/agent-brief.md`, ≤ 100 lines, made by `bootstrap-project`) — not a list of whole skills to read. Agents preload only the one skill they run.
- **Review the delta.** One review per head; findings batched; re-review covers `git diff <reviewed>..HEAD` only; two rounds at most.
- **Test what changed.** Single test and area while iterating; required full suites once on the final head, again only when their inputs change.

## The lifecycle (Structural path; shorter tiers skip the boxes they do not need)

```
idea ──► shape-idea ──► bootstrap-project (repo, protection, tracker, skeleton, AGENTS.md, agent brief, CI)
        │
        ▼
feature from scratch: investigate-feature ──► spec ──► design-review ──► feature-to-issues (when slices are independent)
slice following a reviewed design / change in existing structure: start-issue (inline design check)
bug: file-bug (when tracked) ──► investigate-bug ──► bugfix (design-review if the fix creates structure; focused review if it touches a high-risk area)
        │
        ▼
 implement (feature | bug | maintenance) — area skills only for parts touched
        │
        ▼
 pre-commit ──► create-pr ──► code-review at the tier's depth ──► ci ──► deploy-check (when touched)
        │
        ▼
 merge (gates per tier; the merging session reads the diff) ──► release ──► observe ──► cleanup
                  incident ──► postmortem ──► capture-lesson ──► create-skill
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
| Review a plan before code (Structural / High-risk only) | `design-review` (+ `architect` agent) | lifecycle (+ agents) |
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
| Collapse repeated switches over a closed set | `static-catalogs` | quality |
| Choose the tier and brief subagents | `work-context` | foundation |
| Constrain agent access, untrusted content | `safe-agent-execution` | foundation |
| Model-backed features, retrieval, tool agents | `llm-integration` / `rag-pipeline` / `agent-workflow` | ai |
| Architecture from scratch / large refactors | `system-design` / `safe-refactoring` | architecture |
| Pipelines, database operations, ML lifecycle | `data-pipeline` / `database-operations` / `ml-lifecycle` | data |
| Threat model, identity and access, supply chain | `threat-model` / `identity-access` / `supply-chain` | security |
| SLOs, infrastructure changes, restore drills | `service-reliability` / `infrastructure-change` / `recovery-drill` | operations |
| Desktop apps, memory/FFI, concurrency/networking, specialist domains | `desktop-application` / `memory-and-ffi` / `concurrency-networking` / `specialized-engineering` | desktop, systems, specialist |
| Create or update a skill / record a decision / encode a lesson | `create-skill` / `decision` / `capture-lesson` | meta |

## Shared rules (every skill inherits these)

- **The project wins** on facts (commands, paths, names) and policy (issue-first, who merges, attribution, strict review). A team that wants every change tracked and independently reviewed says so in `AGENTS.md`; skills then apply that at every tier.
- **The tier decides the ceremony**; it never removes a control the tier requires. Structural / High-risk work always gets a design review before code, failure-path tests and an independent review with a design pass.
- **Tests first for new behaviour.** A behaviour change without a test that fails without it is not done; docs, config and generated output use their own checks.
- **The speed rule:** speed may cut test reruns, review rounds and ceremony the tier does not require — never the tests written, a Structural change's design review, or the design pass its tier requires.
- **Safety-critical paths** get failure-path tests, never swallow errors, and their PR explains the failure mode.
- **Personal data** is never logged at shipped levels, sent to third-party analytics, or pasted into issues, PRs, commits or test names.
- **Outward-facing actions** (issues, comments, pushes, PRs, merges, releases) need authorization unless the request or the project's policy gives it. Opening a PR does not authorize merging; a no-merge instruction is binding.
- **Evidence binds to the candidate:** tests, reviews and deploy checks name the commit they cover; a later change invalidates what it touches. A comment title or self-authored timestamp is not proof.
- **Report states precisely:** implemented, verified, PR open, CI green, merged, released.
- **Lessons are encoded, not remembered:** a check, a gate, a rule, or a line in the agent brief.
