---
name: work-context
description: "Pick the right amount of process for an engineering change and reuse what is already known. Classifies the task Quick, Standard or Structural/High-risk with concrete triggers, says which steps, reviews, subagents and test runs each tier gets, keeps a short task card so nothing is re-read, and briefs subagents with a digest instead of whole skills. Use at the start or resumption of any code change. Trigger on 'how much process', 'is a design review needed', 'quick fix', 'small change', 'why is this so slow', 'risk tier'."
license: MIT
metadata:
  version: "1.0.0"
---

# Work context

Decide once per task how much process `$ARGUMENTS` needs, write it down in a short task card, and reuse that card until the facts change. Every other skill reads its tier from here instead of running its full procedure by default. This skill selects steps; it never grants authority.

## 0. Read the project

Read the project's agent rules (`AGENTS.md`, `CLAUDE.md` or equivalent), the **agent brief** if the project has one (§3), working-tree status and the code the task touches. Find the actual commands. Project rules win: if the project requires an issue, a design review or a reviewer for every change, do that — the tier then only decides depth.

## 1. Classify the task

Classify by **what the change creates and what a mistake would cost**, not by line count. Take the first row that matches; when discovery changes the answer, re-classify and say so.

| Tier | Triggers (any one) | Not this tier |
|---|---|---|
| **Structural / High-risk** | A new feature or module from scratch · a new layer, service, package or app boundary · a new or changed data model, migration or stored format · a new public resource or event type, or a **breaking** contract change (removed or renamed field, changed meaning, new required input) · a new dependency or framework · a cross-cutting refactor (several features or layers) · an area the project declares high-risk (auth and permissions, money, personal data, safety-critical, destructive data, delivery guarantees, background execution, release signing) | — |
| **Standard** | New or changed behaviour **inside existing structure**: a feature slice that follows an existing pattern, a bug fix in existing code, a new screen state, a new endpoint in an existing resource, an **additive** optional field or query parameter, a new test-backed rule | Anything above |
| **Quick** | No new behaviour, or a tiny reversible one with no trigger above: copy, styling, a UI tweak within an existing component, docs that change no rule, comments, test-only changes, config/tooling, a patch-level dependency bump, a rename inside one module, a one-line fix whose cause is already known | A one-line change to a permission, an access or tenant filter in a query, a retry or a safety path — that is High-risk. Config that touches security headers, CORS, CI permissions, deploys, feature flags or runtime behaviour is at least Standard. Removing or weakening a failure-path test, a lint, an architecture test or a hook is High-risk, and so is changing the rules themselves: a merge gate, the tier rules, the high-risk list or a review or testing rule (agent rules files, agent definitions, the build/check entry point). |

**Structural vs High-risk.** Both get the right-hand column. A High-risk change that creates **no** structure (a one-line fix on a safety path, a retry or permission fix) runs it in focused form: no spec, the plan states the failure modes and the rollback in a few lines, and the design review answers only failure modes, tests and recovery (`design-review` questions 7 and 9).

**Path floor.** A project may list paths whose changes are at least Standard or High-risk (for example the shared core, native background code, migrations, contracts, auth, hooks and lint rules); a tool or the reviewer applies it from the diff. The reviewer re-checks the tier: a tier too low for what the diff touches is a `major` finding. A tier raised mid-work stops coding until that tier's missing steps (for example the design review) are done.

Already-clean, already-reviewed code that the diff does not restructure is **not** re-reviewed for design. A new screen built from existing components is Standard; a new navigation model is Structural.

## 2. What each tier runs

| Step | Quick | Standard | Structural / High-risk |
|---|---|---|---|
| Tracker issue | Only if the project requires one | Existing issue or request is enough unless the project requires one | Issue with acceptance criteria |
| Plan | One sentence in the task card | 3–6 lines: behaviour, files, tests | Structural: spec or plan with failure/threat model · High-risk without structure: failure modes and rollback in the plan |
| Design review | None | **Inline design check** by the implementer: placement, reuse, next feature, tests (§2a) | **Separate `design-review` before code** (architect agent when available) |
| Tests | Targeted check for what changed; a regression test for a behaviour fix | Test-first for new behaviour (`tdd`); targeted runs while working | Test-first with failure paths first; negative, crash and compatibility tests |
| Full suites | Once, before commit, for the touched area | **Once on the final head** | Once on the final head, plus platform/device/data checks that apply |
| Review | Self-review of the diff with the `code-review` short checklist | **One** independent review at the end (reviewer agent with a brief, §3) | Independent review with a full design pass; `security-privacy-review` when personal data, auth, sharing, uploads, payments or analytics are touched |
| Subagents | None | At most one (reviewer) | Architect before, reviewer after, tester for gaps |
| Recovery plan | — | Rollback is "revert the commit" | Written rollback/recovery plan (one line when a revert is safe; full plan for data, contract or release changes) |

### 2a. The inline design check (Standard)

Answer in the plan, in one line each: **Placement** — which existing file/layer gets each piece? **Reuse** — what existing component, query or helper did you search for and reuse? **Next feature** — would the next feature of the same kind (one that exists or is planned) have to write this again? **Tests** — which behaviours get which tests? If an answer needs a new layer, abstraction, contract or data shape, the task is Structural: stop and run `design-review`.

### 2b. Review and test loops

- One review per candidate head. Findings come back **batched**; fix them all, then re-review **only the delta** (`git diff <reviewed-head>..HEAD`) unless a fix changed structure.
- At most **two** review rounds; a third means the plan was wrong — stop and re-plan with the user. The cap never lets a finding stay open: it means re-plan, never merge.
- While iterating, run only the tests for what changed. Re-run a full suite only when its inputs changed since its last green run. A docs-only or test-only fix does not re-run unrelated suites.
- Never skip a check the project or the tier requires to save time; skip only what neither requires.

## 3. Read once, brief others

Re-reading the same long instructions is the largest avoidable cost in agent work.

- **In this session:** a skill, reference or file already read is not read again unless it changed or the conversation was compacted — then read only the section you need. Load a skill's `references/` only when the step you are on needs them.
- **The task card** (kept in the conversation, ≤ 15 lines): outcome, tier and why, files, commands, acceptance criteria, decisions, checks run with results, open questions. Update it; do not re-derive it.
- **The agent brief** (`docs/agent-brief.md` in the project, ≤ 100 lines, created by `bootstrap-project`, kept current by `capture-lesson`): commands per area, the placement map, naming, the high-risk areas list and the rules reviews keep finding. It is the condensed form of the conventions skills for *this* project.
- **Subagents start with no memory of this conversation.** Hand them a brief, not a reading list: the task card, the diff or plan, the agent brief (or the 10–20 rules that apply), and the one skill they run. Tell them which reference sections to open *if* needed. Never tell a subagent to read every conventions skill.

## 4. Evidence and handoff

Record what changed, the checks actually run with their results, the reviewed revision and what is unverified. Keep **implemented, verified, PR open, CI green, merged, released** distinct. Before merge or release, check the candidate head is the one that was verified and reviewed.

## Rules

- Classify before working; a low-risk task never inherits High-risk ceremony because a generic skill mentions it, and a High-risk task never loses its gates to save time.
- Project rules beat this table; explain a conflict, never weaken a required control silently.
- Never fabricate a passing test, an independent review or an approval.
- Do not create tracker or process artifacts that neither the project nor the tier asks for.

## Composition

| From | This skill | To |
|---|---|---|
| Any engineering task, resumed work | Tier, task card, brief for subagents | `implement`, `bugfix`, `new-feature`, `design-review` (Structural only), `code-review` at the tier's depth |
