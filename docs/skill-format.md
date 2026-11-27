# Skill format (the house structure)

Every skill in this repository follows the open [Agent Skills](https://agentskills.io/specification) format, so Claude Code and other agents can load it, plus the house structure below. `scripts/check.py` enforces the mechanical parts in CI.

## Files

```
plugins/<plugin>/skills/<skill-name>/
├── SKILL.md              # required: frontmatter + the procedure, under ~250 lines
└── references/           # optional: stack-specific or long reference material
    ├── <stack>.md        # e.g. dotnet.md, django.md, node.md, spring.md, flutter.md, react-native.md, kotlin.md, swift.md
    └── <topic>.md        # e.g. design-patterns.md
```

- `name` is lowercase letters, digits and single hyphens, at most 64 characters, and equal to the folder name.
- `description` is at most 1024 characters (the Agent Skills limit; Claude Code allows more, we keep to the smaller one).
- References are one level deep and linked from `SKILL.md` with a relative link: `[references/django.md](references/django.md)`.

## Frontmatter

```yaml
---
name: <kebab-name>
description: "<What it does, in one sentence> — <the key steps>. Use when <situation>. Trigger on /<name>, '<phrase people say>', '<another>'."
argument-hint: "[what the argument is]"     # optional
license: MIT
metadata:
  version: "1.0.0"                           # the plugin's version; bumped with the plugin
---
```

The description is how an agent picks the skill. List the phrases people actually say. Put the main use first.

## Body

```markdown
# <Title>

<One line: what it does for `$ARGUMENTS` (say what the argument is)>. If `$ARGUMENTS` is empty, <ask what / the default>.

## 0. Read the project
<The project's own rules first: AGENTS.md / CLAUDE.md / CONTRIBUTING.md, its conventions, its stack manifest.
Which facts this skill needs from them (commands, paths, tracker, labels). The project wins on facts; when a fact is
missing, ask once and offer to record it in AGENTS.md.>

## 1. <Phase>
Numbered steps. Commands in code blocks, as examples to adapt, never as facts about the user's repo.
**Gate:** <what must be true before the next phase> (wherever a wrong move is costly)

## Rules
- What never to do; what needs the user's OK; safety and privacy limits.

## Composition
| From | This skill | To |
```

## House rules

1. **Framework-agnostic core.** `SKILL.md` bodies never assume a framework, language or vendor (no .NET, Django, Rails, Spring, Node frameworks, React, Flutter, Kotlin, Swift …). Speak in layers, ports and adapters, tests, contracts. Stack detail that genuinely helps goes in `references/<stack>.md`. `scripts/framework-terms.txt` lists the names CI rejects in `SKILL.md` bodies.
2. **Read before acting.** Phase 0 reads the target project's conventions; the skill adapts to them. Never invent paths, commands or tools: discover them (`ls`, the manifest, the CI file) or ask.
3. **Gates where a wrong move is costly.** A gate names a checkable condition, not a feeling.
4. **Reference, don't copy.** A skill points to the skill that owns a rule (`testing-doctrine` owns test rules, `engineering-principles` owns placement) instead of restating it. When the owning skill is in another plugin, name the plugin: "`testing-doctrine` (quality plugin)".
5. **GitHub is the default example tracker** (`gh` commands); every skill says "or the project's tracker" and reads the real one from `AGENTS.md`. Git itself is assumed.
6. **Outward-facing actions need the user's OK** (issues, labels, comments, pushes, PRs, releases, messages), unless the user's request already gave it. Merging follows the project's merge gates.
7. **Safety and privacy rules are never weakened by a skill.** Safety-critical paths (the project's list in `AGENTS.md` wins; by default anything where a silent failure can harm a person, lose money or lose or corrupt data) get failure-path tests first and never swallow errors.
11. **One rung ladder.** "Where should this have been caught" uses the ladder defined in `testing-doctrine` (quality plugin); skills point to it instead of restating a different one.
12. **Installed skills are a cache.** A skill that changes skills (`create-skill`, `capture-lesson`, `postmortem`) distinguishes the consumer project (encode lessons locally, draft an upstream issue) from this repository.
8. **Short and complete.** Long tables and checklists go in `references/`.
9. **Examples are generic.** Toy domains only (a notes app, an online shop, a booking system). No real product, person, company, issue number, internal path or URL.
10. **Every claim is checkable.** "Tests pass" only with the command and its output.

## How a skill is checked

- `python3 scripts/check.py` — frontmatter, names, description length, JSON manifests, versions, relative links, framework names in `SKILL.md` bodies, privacy patterns.
- `claude plugin validate . --strict` and `claude plugin validate plugins/<plugin> --strict`.
- A fresh-agent dry run on a realistic task (`create-skill` §3).

## Catalogue contract

[The schema](../schemas/catalog.schema.json) describes `catalog/skills.json`. Required dependencies form an acyclic availability graph; optional companions/workflow transitions are separate. Resources include all supporting files. `scripts/check.py catalog` checks metadata, versions, graph and file parity. Frontmatter is strict YAML: duplicate keys, aliases, unsafe tags and non-string metadata are rejected.
