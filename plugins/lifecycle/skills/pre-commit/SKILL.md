---
name: pre-commit
description: "Check the working tree and commit it safely — not on the main branch, named paths staged only, secrets and personal-data scan, generated code in sync with its source, only touched files formatted, the project's lint/analyze/test run for each changed area, a safety-critical check, and a conventional commit that follows the project's author and attribution policy. Never bypasses hooks. Use when about to commit. Trigger on /pre-commit, 'commit this', 'check before committing', 'is this ready to commit', 'stage and commit'."
argument-hint: "[commit message or scope]"
license: MIT
metadata:
  version: "1.0.0"
---

# Pre-commit

Check the working tree and commit `$ARGUMENTS` (an optional commit message or scope). Run every step that applies to the changed paths; skip a step only when no file it covers changed, and say so.

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`: the **commands per area** (format, lint/analyze, test, build), the code generators, the commit message convention, and the **author and attribution policy** (who commits; whether AI co-author trailers or "generated with" lines are allowed).
2. Read the hooks the repo already has (`.git/hooks`, a hooks manager config, agent hooks) so you know what runs automatically — and what it does not catch.
3. A fact you need is missing (e.g. no test command for an area) → ask once and offer to add it to `AGENTS.md`.

## 1. Where am I

```bash
git branch --show-current        # must not be the main branch
git status --short
git diff --stat; git diff --cached --stat
```

On the main branch → stop. Create a branch (`start-issue` naming) and move the changes there.

## 2. What goes in

Stage **named paths only** — never `git add -A` / `git add .`. Leave out build output, dependency folders, local config (`.env*`, local properties), keystores and signing files, platform credential files, screenshots with real data, scratch files. Something that should never be committed and is not ignored → add it to `.gitignore` in its own commit.

**Gate:** `git diff --cached --name-only` lists only files that belong to this change.

## 3. Secrets and personal data

```bash
git diff --cached | grep -nEi '(api[_-]?key|secret|password|passwd|token|BEGIN [A-Z ]*PRIVATE KEY)' || true
git diff --cached | grep -nE '[-+]?[0-9]{1,2}\.[0-9]{4,},\s*[-+]?[0-9]{1,3}\.[0-9]{4,}' || true   # lat,lng pairs
git diff --cached | grep -nEi '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' || true                      # emails
```

Check every hit by hand. A real secret → unstage, remove, move it to configuration, and tell the user (rotate it if it was ever pushed). Personal data (real names, emails, phone numbers, addresses, precise locations) is allowed only as obviously synthetic test fixtures. The `guardrails` plugin's hook blocks common key shapes at commit time; it does not replace this step.

## 4. Generated code is in sync

For each source of generated code the diff touched, run its generator and stage the output (the commands are in `AGENTS.md`):

| If this changed | Regenerate |
|---|---|
| API contract (OpenAPI, GraphQL schema, protobuf) | client/server stubs |
| String resources / translation files | generated localisation code |
| Native bridge definitions | both sides of the bridge |
| Annotated models / codegen sources | generated model files |
| Database models | the migration (`add-migration`, backend plugin) |

Never hand-edit generated files. **Gate:** regenerating produces no further diff.

## 5. Format, lint, test — per changed area

1. **Format only the hand-written files this commit touches** (never reformat untouched files in a feature commit; generated files are formatted by their generator).
2. For each area the diff touches (`git diff --cached --name-only`), run that area's lint/analyze and tests from `AGENTS.md`. Integration tests need the project's local services running.
3. Re-stage files the formatter changed.

**Gate:** every command exits 0, with its output kept for the report. A failing check is fixed, never bypassed.

## 6. Safety-critical check

If the diff touches a safety-critical path (the project lists them; by default anything where a silent failure can harm a person, lose money or lose data): a failure-path test is in this commit or earlier on the branch (`testing-doctrine`, quality plugin), and no catch swallows an error without logging and surfacing it.

## 7. Commit

Conventional message, imperative, subject ≤ 72 characters: `type(scope): summary` with type `feat|fix|refactor|perf|test|docs|build|ci|chore|style` and a scope naming the area or topic. The body says **why** when it is not obvious, and references the issue (`Refs #<issue>`; the closing keyword goes in the PR or the last commit).

```bash
git commit -m "feat(api): reject orders with more than 50 lines" -m "Refs #<issue>"
git log -1 --format='%an <%ae>%n%B'      # check the author and the message
```

Follow the project's author and attribution policy exactly. If it forbids AI co-author trailers or "generated with" lines, check the final message yourself — a hook that scans the command line does not see a message read from a file.

## Rules

- Never `--no-verify`, never skip or disable a hook to get a commit through.
- Small commits: one logical change each; refactor and behaviour change in separate commits.
- Do not push here; pushing and PRs belong to `create-pr`.
- Never stash in a repository shared by several worktrees or sessions; commit work in progress on its branch instead.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `tdd` (quality), `bugfix` | Checks + commit | `create-pr` |
| `guardrails` plugin hooks | Automatic backstop for secrets and main-branch commits | — |

## Report

What was checked (command → result), what was skipped and why, the commit hash.
