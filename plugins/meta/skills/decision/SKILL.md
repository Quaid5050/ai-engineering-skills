---
name: decision
description: "Record an architecture or engineering decision as a short decision record (ADR) — context with paths, at least two real options including keeping what exists, each with cost now, cost later, what it locks in and an authoritative source, the decision, consequences and follow-up edits, and a concrete 'revisit when' signal — then link it from the convention it explains; or amend/supersede an old record. Use when adopting or refusing a library, pattern, structure, service or stance that is costly to reverse. Trigger on /decision, 'record this decision', 'write an ADR', 'why did we choose X', 'should we switch to Y', 'decision record'."
argument-hint: "[the question, e.g. 'which database?']"
license: MIT
metadata:
  version: "1.0.0"
---

# Decision

Record the decision `$ARGUMENTS` (the question). If empty, ask which decision to record.

## 0. Read the project

- Where records live (`docs/decisions/`, `docs/adr/`, or as the project says) and the format of the newest one; numbering.
- The conventions skill or doc the decision shapes, and earlier records on the same topic.

## 1. Is a record needed?

Write one when a choice is **costly to reverse or easy to forget the reason for**: adopting or refusing a dependency, a structural pattern, a new module or service, a data or API convention, a security or privacy stance, a paid or third-party service. Not for choices a convention already fixes, or that a refactor can undo in an hour.

## 2. Research

- The problem in this repository, with paths, and who it affects (users, battery, cost, privacy, the team).
- At least **two real options, including "keep what we have"**. For each: cost now, cost later, what it locks in, and an authoritative source (official documentation first).
- Reopening an existing record? First check its **Revisit when** condition with evidence. Not met and nothing new argues otherwise → the outcome is "keep": add a dated line to the old record's Revisit section and stop.
- The follow-up edits the decision forces (conventions, manifests, generators, lint configuration, related records).

**Gate:** a record that lands with the work it decides is written `accepted` in that change (merging is the acceptance); `proposed` only for a record put up for discussion first. A record that adds or removes a dependency, changes product behaviour, safety-critical code or privacy, or adds a paid service needs the owner's agreement in the conversation (quote them in the PR).

## 3. Write `docs/decisions/NNNN-<kebab-slug>.md`

Next free number, four digits.

```markdown
# NNNN — <Decision as a short statement>

**Status:** proposed | accepted | amended by NNNN | superseded by NNNN · <YYYY-MM-DD>

## Context
<The problem and the forces, 3–6 lines, with paths.>

## Options
| Option | For | Against |
|---|---|---|
| <A (chosen)> | … | … |
| <B> | … | … |
| Keep what we have | … | … |

## Decision
<What we do, in one paragraph. What we do not do.>

## Consequences
- <What gets easier / harder; follow-up work with issue links.>

## Revisit when
<The concrete signal that should reopen this: a size, a version, a cost, a pain point.>

## Sources
- <title>: <url>
```

## 4. Link and land

- Link the record from the convention or skill whose rule it explains.
- Replacing a whole record: set the old one to `superseded by NNNN`. Changing one choice inside a record that bundles several: write a new record for that choice and set the old one to `amended by NNNN`, naming the line it replaces. Link both ways; never delete a record.
- Make the follow-up edits in the same change, or file them as issues linked from Consequences.
- It lands like any change: issue → branch → PR → `code-review` (quality plugin).

## Rules

- Facts with sources; no option dismissed without a reason.
- One decision per record, at most a page; coupled choices may share a record only as separate lines, so each can be amended alone.
- A record never weakens the project's safety, privacy or testing rules.

## Composition

| From | This skill | To |
|---|---|---|
| `bootstrap-project` (stack), `design-review` (costly-to-reverse choices), `spec`, the user | An accepted record linked from its convention | The convention or skill it shapes |
