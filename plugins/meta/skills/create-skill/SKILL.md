---
name: create-skill
description: "Create or update an agent skill in the house structure — research the real workflow, commands and paths, check overlap with existing skills (compose, don't duplicate), draft SKILL.md with a trigger-rich description, a read-the-project phase, numbered phases with gates, rules and composition, keep stack detail in references/, then have a fresh agent dry-run it on a realistic task and fix every real gap, and register it. Works for a project's own skills and for this marketplace. Trigger on /create-skill, 'add a new skill', 'turn this into a skill', 'update the skill', 'improve this skill', 'the skill was wrong', 'write a SKILL.md'."
argument-hint: "[workflow description, skill name to update, or a lesson]"
license: MIT
metadata:
  version: "1.0.0"
---

# Create skill

Create or update the skill for `$ARGUMENTS` — a workflow description, the name of a skill to update, or a lesson ("the review missed X"). A lesson from a real project goes through `capture-lesson` first; it calls this skill for the edit. If empty, ask which workflow the skill should cover.

## 0. Read the project

- Where skills live here: a project's `.claude/skills/<name>/SKILL.md` (or the agent's equivalent), or this marketplace's `plugins/<plugin>/skills/<name>/SKILL.md`.
- Installed plugin skills are a cache: in a project that installed this marketplace, create or change the **project's own** skills (e.g. `.claude/skills/`), never the plugin files; propose marketplace changes as an upstream issue (`capture-lesson`).
- The house structure: this marketplace's `docs/skill-format.md`, or the project's own skill guide if it has one. The workflow map (`docs/engineering-workflow.md` or equivalent) and the shared rules (`AGENTS.md`).

## 1. Research

1. **Scope:** what triggers it (words people say, an event), where it runs (local, CI, staging, production), what it touches (git, tracker, code, database, devices), what it outputs (code, issue, report, comment).
2. **Facts from the repository, not memory:** exact commands, paths, job names, config keys — read the files (CI workflows, manifests, scripts); run read-only commands to confirm they work.
3. **Overlap:** list the existing skills and read the ones in the same lifecycle step. Do not duplicate — compose. If an existing skill almost covers it, update that one.
4. **Standards to reference, not copy:** the skill that owns each rule (`testing-doctrine` for tests, `engineering-principles` for placement, `security-privacy-review` for the logging rule).

**Gate:** you have the real commands and paths, the skills it composes with, and the rules it references.

## 2. Draft

```markdown
---
name: <kebab-name>                       # = folder name; lowercase, digits, single hyphens, ≤ 64 chars
description: "<what it does> — <key steps>. Use when <situation>. Trigger on /<name>, '<phrase>', '<phrase>'."   # ≤ 1024 chars
argument-hint: "[what the argument is]"
license: MIT
metadata:
  version: "<plugin version>"
---

# <Title>
<One line: what it does for `$ARGUMENTS`>. If `$ARGUMENTS` is empty, <ask / default>.

## 0. Read the project
## 1. <Phase>            (numbered steps; commands in code blocks as examples to adapt)
**Gate:** <checkable condition>   (wherever a wrong move is costly)
## Rules
## Composition
| From | This skill | To |
```

House rules:
- The **description** is how the skill gets picked: the main use first, then the phrases people actually say.
- **Read before acting:** Phase 0 makes the skill adapt to the project; the project wins on facts.
- **Framework-agnostic core** (for shared skills): no framework, language or vendor names in `SKILL.md`; stack detail in `references/<stack>.md`, linked from the body.
- Real paths and commands only; anything not built is marked "not wired yet — set it up as its own issue the first time and update this skill".
- Reference other skills instead of copying their rules.
- Say what is outward-facing (issues, PRs, comments, releases, messages) and that it needs the user's OK.
- Safety and privacy rules are never weakened by a skill.
- As short as it can be while complete; long tables go in `references/`.
- Generic examples only — no real product, person, issue number, internal path or URL.

## 3. Fresh-agent dry run

Spawn a fresh agent (no conversation history) with only: the skill path, `AGENTS.md`, and a **realistic task** for the skill ("file a bug: orders placed offline are submitted twice after reconnect"). Ask it to walk through the skill without outward-facing actions and report: ambiguous steps, commands that fail or do not exist, missing decisions, places it had to guess, contradictions with other skills. Fix every real gap; list the rejected ones and why in your reply.

For a framework-agnostic skill, run the dry run **twice, on two different stacks**, and check that nothing in the core text only made sense for one of them.

**Gate:** a second dry run (or the same agent re-checking) finds no new real gap.

## 4. Validate and register

- Run the checks: this marketplace's `python3 scripts/check.py` and `claude plugin validate <plugin dir> --strict`; or the project's own skill lint.
- Register it: a row in the workflow map's "which skill when" table (and the lifecycle diagram if it is a lifecycle step), the skill list in `AGENTS.md`/`CLAUDE.md`, and — in this marketplace — the README catalogue, the plugin's version bump and a `CHANGELOG.md` entry.
- Commit on a `docs/` or `chore/` branch: `docs(skills): add <name>` / `docs(skills): update <name> — <lesson>`.

## Updating a skill

When a skill was wrong (a command changed, a step missed a bug, a postmortem follow-up): fix the exact line, add the missing check **where it would have caught the problem**, and say in the commit body what went wrong. The code wins over the skill on facts; keep them in sync. A change that alters a gate or a rule others rely on is a MINOR version bump of the plugin; a removed or renamed skill is MAJOR (`CONTRIBUTING.md`).

## Rules

- Never register a skill that has not had a fresh-agent dry run.
- Never weaken a safety, privacy or testing rule to make a skill shorter.
- Do not copy another skill's rules; link to the owner.

## Composition

| From | This skill | To |
|---|---|---|
| `capture-lesson`, `postmortem`, the user | A new or updated, dry-run skill | `decision` when the skill encodes a costly choice |
