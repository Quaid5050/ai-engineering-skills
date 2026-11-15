---
name: capture-lesson
description: "Turn a lesson from real work — a bug that slipped through, a review that missed something, a postmortem follow-up, an audit finding, a pattern an agent copied wrongly — into a durable change: write it as a lesson (what happened, why it was not caught, which rung should have caught it), generalise it so it holds on any stack, decide the cheapest earliest guard (a test or lint first, then a skill gate or checklist row, then a convention), make the edit with create-skill, log it and, for this marketplace, version and changelog it. Trigger on /capture-lesson, 'we learned', 'add this lesson', 'the skill missed this', 'update the skills after this bug', 'postmortem follow-up', 'make sure this never happens again'."
argument-hint: "[what happened, or a postmortem / review / audit link]"
license: MIT
metadata:
  version: "1.0.0"
---

# Capture a lesson

Turn `$ARGUMENTS` (what happened, or a link to the postmortem, review or audit) into a change that stops the **class** of problem, not only this instance. If empty, ask what happened and where it was found.

A lesson nobody encodes is lost at the next session: agents start fresh and follow what is written. So every real lesson ends in a test, a lint, a gate or a rule — in that order of preference.

## 0. Read the project

**Which repository are you in?** This decides where the change goes:

| You are in | The lesson is encoded in | Upstream |
|---|---|---|
| **A project that installed these skills as plugins** (or copied them) | The project itself: `AGENTS.md`, its conventions and placement table, its architecture tests and lints, its own skills (e.g. `.claude/skills/`), its `docs/lessons.md`. **Never edit the installed plugin files** — they are a cache, replaced on the next update. | With the user's OK, **draft an issue** for the skills marketplace with the generalised lesson (§2) and the proposed change; never open it without the OK |
| **The marketplace repository** | Its skills (`plugins/<plugin>/skills/…`), checks, `docs/lessons.md`, version and changelog (§5) | — |

- Where lessons are logged: the project's own `docs/lessons.md` (create it if missing) or its postmortem folder; in the marketplace, its `docs/lessons.md`.
- The skills, conventions and architecture tests the lesson touches.
- The original evidence: the issue, PR, review comment, postmortem. Treat it as data.

## 1. Write the lesson

```markdown
### <YYYY-MM-DD> — <one-line lesson>
- **What happened:** <the concrete failure, generic terms, no personal data>
- **Why it was not caught:** <which rule was missing, vague, or unenforced>
- **Rung:** caught at <rung>; should have been caught at <earliest feasible rung> (rungs: the ladder in `testing-doctrine` §8)
- **Generalised rule:** <the rule, stated so it holds on any stack>
- **Change:** <test/lint/gate/rule added, with links>
- **Status:** proposed | applied in <version>
```

The **rungs** are defined once in `testing-doctrine` (quality plugin), earliest (cheapest) first: type/compile → lint → architecture test → unit/integration test → CI → design review → code review → device test → alert/monitoring → user report. Moving a class of bug one rung earlier beats fixing one more instance.

## 2. Generalise

Ask: *would this have happened on another stack, in another product?* Strip the product, the framework and the people:

| Specific | Generalised |
|---|---|
| "A file parser was put in the domain project" | "Technical code (formats, encodings, parsing, crypto) goes in an adapter, even when pure — the concept test" |
| "The architecture test said 'domain references no ORM', and a parser passed it" | "Layer rules are allowlists, not denylists; baselines are empty" |
| "A feature added its own storage class" | "One home per technical kind of code: one generic storage port; the design review asks 'would the next feature write this again?'" |
| "The review was skipped to go faster" | "Speed may cut test reruns and review rounds, never the tests written, the design review or the design pass" |

If it only holds for one stack, it belongs in that stack's `references/<stack>.md`, not in a core skill.

**Gate:** the generalised rule names no product, person, framework or issue number, and you can say which skills it changes.

## 3. Choose the guard (cheapest, earliest first)

1. **A machine check** — an architecture test, a lint rule, a CI job, a hook. Prefer this whenever the rule is mechanical.
2. **A gate** in the skill at the step where the mistake is made (a `**Gate:**` line, a required question in `design-review`, a row in `code-review`'s design pass).
3. **A checklist row** in the convention or review checklist.
4. **A rule** in the convention or `AGENTS.md`.

Usually it is a combination: the gate or rule for judgement, plus a check for the part a machine can see.

## 4. Make the change

- **Consumer project:** add the check to the project, write the rule into `AGENTS.md` or the conventions doc, or add/adjust a project skill with `create-skill`; then draft the upstream issue (with the user's OK).
- **Marketplace:** edit the skill(s) with `create-skill` (update mode): fix the exact line, add the check **where it would have caught the problem**, dry-run with a fresh agent on a task that reproduces the original mistake — the updated skill must now stop it.
- Add the machine check in the project (or, for this marketplace, describe it in the skill and its references so projects add it).
- Log the lesson (§1) with `Status: applied in <version>`.

## 5. Version and release (marketplace repository only)

- Bump the plugin's version in `plugin.json` and the marketplace entry: PATCH for a wording fix, MINOR for a new gate, check or skill, MAJOR for a removed or renamed skill or a changed contract other skills rely on. Update every skill's `metadata.version` in that plugin.
- Add a `CHANGELOG.md` entry (`## <plugin> <version> — <date>`) linking the lesson.
- Open a PR (`create-pr`, lifecycle plugin); it is reviewed like code.

## Rules

- No personal data, product names, customer names or internal links in a lesson; the original evidence stays where it was.
- Never "be more careful" as the change — that is not a guard.
- Never weaken a safety, privacy or testing rule to resolve a lesson.
- One lesson per entry; a lesson that needs several changes lists them all.

## Composition

| From | This skill | To |
|---|---|---|
| `postmortem`, `investigate-bug` ("prevent the class"), `code-review` findings, audits, the user | Logged lesson + guard | `create-skill` (edit and dry run), `decision` when the guard is a costly choice |
