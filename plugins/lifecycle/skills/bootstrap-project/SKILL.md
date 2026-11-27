---
name: bootstrap-project
description: "Set up a new repository so agents can build it safely from day one — create the repo and an initial commit, protect main, set up the tracker (milestones, labels, templates) and a bootstrap issue, then on its branch record the stack decisions, build a walking skeleton (one request end to end, one scheduled job when the product needs one, deployed to a test environment), write AGENTS.md with the real commands, safety-critical paths and rules, install the placement table and allowlist architecture tests with reviewed legacy baselines with no new violations, lint/format, CI on hosted runners, and open the PR that closes the issue. Covers web and mobile setup. Use after shape-idea, or when an existing repo has no agent rules, conventions or CI. Trigger on /bootstrap-project, 'set up the repo', 'start a new project', 'scaffold the app', 'add AGENTS.md', 'make this repo agent-ready'."
argument-hint: "[product name or path to the brief]"
license: MIT
metadata:
  version: "2.0.0"
---

# Bootstrap a project

Make the repository for `$ARGUMENTS` (a product name, or the brief) ready for agent-driven work. If empty, ask for the brief or run `shape-idea` first.

Agents follow written rules and copy the code next to them. A repository with no rules teaches them whatever the first file does, so the rules, the checks and the first good example come **before** the features.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

- The brief and MVP scope from `shape-idea` — from `docs/product/` if a repository exists, otherwise **from the conversation or the scratch folder** where `shape-idea` left them. None anywhere → run `shape-idea` first.
- An existing repository: read `README.md`, the manifests, CI files, `AGENTS.md`/`CLAUDE.md`. Keep what exists and works; skip the steps that are already done.
- The owner's constraints (hosting, budget, team skills, platforms) decide the stack, not fashion.

## 1. Repository and protection

With the owner's OK (all of this is visible to others):

1. Create the repository; the owner chooses **public or private**. Example: `gh repo create <owner>/<name> --private --clone`.
2. An initial commit on `main` (README stub, `.gitignore`, licence) so there is a base to branch from. If the `guardrails` plugin is enabled, allow this one commit with a command prefix: `GUARDRAILS_ALLOW_MAIN_COMMIT=1 git commit -m "chore: initial commit"`. Push it.
3. Protect `main`: a branch protection rule or ruleset requiring pull requests and the CI checks (added in step 6 by name). Enable dependency updates (for example Dependabot) and secret scanning where the host offers them.

## 2. Tracker

- Milestones from the MVP scope (`A — Foundations`, …).
- Labels (script: [references/labels.md](references/labels.md)): type, priority, area, flags (`safety-critical`, `privacy`, `needs-device-test`, `needs-design`), blockers, `in-progress`, `spike`; `feature:<slug>` labels are created per feature by `feature-to-issues`.
- Issue templates (feature, bug) matching `file-feature` and `file-bug`; a PR template matching `create-pr`.
- A **bootstrap issue** (`chore: bootstrap the repository`, milestone A) and its branch from the issue (`chore/<n>-bootstrap`, `start-issue` naming). Everything below lands on that branch, so the bootstrap PR passes the same issue gate as every later PR. Bootstrap is infrastructure, not a feature: its design review is the stack decision records of step 3.

## 3. Product files and stack decisions

1. Commit the brief and MVP scope into `docs/product/brief.md` and `docs/product/mvp-scope.md`.
2. For each costly-to-reverse choice — server language and framework, database, client stack (web / cross-platform mobile / native), hosting, auth provider, CI — write a decision record with `decision` (meta plugin): at least two real options, the trade-offs, the choice and when to revisit it. They land in the bootstrap PR.
3. Prefer boring, well-documented tools the owner can hire for. Mark what is **planned** versus **built**.

**Gate:** the owner agreed to each record in the conversation (quote them in the PR).

## 4. Walking skeleton

The thinnest end-to-end path, built test-first, proving the stack works together:

1. One endpoint (for example a health check plus one authenticated read), its contract in the contract file, one integration test against a real database.
2. One client screen or page that calls it, with one UI test.
3. **One scheduled job end to end** (`add-scheduled-job`, backend plugin) when the brief has any time-based behaviour (reminders, expiry, digests) — the scheduler is usually the riskiest infrastructure.
4. Local services in one command; seed data synthetic.
5. A deploy to a **test** environment (not production) with one smoke check. Creating a hosting account needs the owner's OK; the owner enters any payment or credentials.

**Mobile projects also need** (each with the owner's OK; the owner creates accounts and holds keys): store developer accounts, application/bundle ids, signing keys kept out of the repository (CI secrets), build flavours per environment (test vs production API URL), and a macOS machine or hosted macOS runner for iOS builds. Note store-specific waiting periods (some stores require a closed test before the first production release — `release` references).

Folders follow the layers in `engineering-principles` and the stack conventions skill (`backend-conventions`, `mobile-conventions`, `web-conventions`). Each module gets a short `README.md`: what it is, how to run it.

**Gate:** a fresh clone reaches green tests with the commands of step 5, unaided.

## 5. AGENTS.md — the facts every skill reads

Write `AGENTS.md` at the root (and a thin `CLAUDE.md` pointing to it, if the team uses Claude Code). Template: [references/agents-md-template.md](references/agents-md-template.md). It holds: what the product is; the layout; the **commands** table (every command copied from a real run); the tracker, labels, milestones, branch and commit rules; the **merge gates** and who merges (`merge`); the project's **safety-critical paths** (this list wins over any example in the skills) and privacy rules; pointers to conventions, the placement table, decision records and the workflow map. Keep it short — under ~200 lines; stack-specific rules go in path-scoped rule files where the agent host supports them, so they load only when matching files are touched.

**The agent brief** (`docs/agent-brief.md`, ≤ 100 lines, template in [references/agent-brief-template.md](references/agent-brief-template.md)): the condensed, project-specific form of the conventions — commands per area, the placement map, naming, the high-risk areas, and the rules reviews keep finding. Subagents and reviewers get this instead of being told to read every conventions skill (`work-context` §3).

## 6. Conventions, enforcement and CI

1. Copy the placement table from `engineering-principles` ([placement-table.md](../engineering-principles/references/placement-table.md)) into `docs/conventions.md` with the real paths.
2. Add the **architecture tests** for its rows (allowlists, reviewed legacy baselines with no new violations — [architecture-tests.md](../engineering-principles/references/architecture-tests.md)). Prove each can fail (break it once, watch it go red, revert).
3. Linter and formatter with the strict preset; warnings are errors; no blanket suppressions. One command (`make check` or equivalent) runs lint, format check, architecture tests and all suites.
4. CI (`ci` skill and its template): **hosted runners only for a public repository** — never attach a self-hosted runner to a public repo; anyone who opens a pull request can run code on it. Stable job names, path filters, pinned action versions, a "PR links an issue" check. Add the job names to the protection rule from step 1.
5. Optionally enable the `guardrails` plugin hooks (secret scan, no commits on main).

**Gate:** `make check` is green locally and in CI on the bootstrap branch.

## 7. Hand off

Open the PR with `create-pr` (`Closes #<bootstrap issue>`), get the code review from the `reviewer` agent (agents plugin), merge per the gates (`merge`). Then start milestone A's first feature with `new-feature`.

## Rules

- No feature code before steps 1–6 are green: the first feature is the example every later one copies.
- Only real commands in `AGENTS.md` — run each one before writing it down; mark anything not built as "planned".
- Never put secrets in the repository; configuration examples hold placeholders only. Signing keys, store and hosting credentials stay with the owner.
- Creating the repository, accounts, milestones and labels, changing protection rules and pushing need the owner's OK.

## Composition

| From | This skill | To |
|---|---|---|
| `shape-idea` (brief and scope, from the conversation or a scratch folder) | Repo, protection, tracker, bootstrap issue, stack records, skeleton, AGENTS.md, conventions + tests, CI | `new-feature` for the first feature; `decision` (meta) for each stack choice |
