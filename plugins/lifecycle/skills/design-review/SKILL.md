---
name: design-review
description: "The mandatory design review of a plan before any code — run by a fresh architect agent and posted on the issue — answering, in order: placement (which layer and file each part lands in, by placement row), reuse (what already exists, with the searches done), the next feature (would it have to write this again — then design the generic piece now) — spec-level on the epic, slice-level on each slice issue, patterns, data, contract, failure modes, performance, tests; output Decisions, Reuse, Risks, Questions, Costly-to-reverse choices; a finding blocks the branch until the plan changes. Never skipped or shortened for speed. Trigger on /design-review, 'review this design', 'is this plan right', 'architecture review', 'review the plan before I build'."
argument-hint: "[issue number, spec path or plan]"
license: MIT
metadata:
  version: "1.0.0"
---

# Design review

Review the plan for `$ARGUMENTS` (an issue, a spec, or a plan in the conversation) **before** the branch has production code. If empty, review the plan in hand.

**Which review, where:**
| Review | Covers | Posted on |
|---|---|---|
| Spec-level | The whole technical design of a specified feature (from `spec`) | The **epic** (multi-slice), or the docs issue for a single-slice feature |
| Slice-level | What one slice adds — may be short and link the spec-level review when the slice follows it, but always answers questions 1–3 for the slice | The **slice issue**, before its first production-code commit |
| Fix | A non-trivial bug fix: where the fix lands, and whether the bug class needs a shared fix | The **bug issue**; the reproduction test may already be committed |

**Why this is a gate and not advice.** Agents follow written rules and copy the code next to them. Tests check names and imports; they rarely check whether a new class is the *right kind of code in the right place*. A wrong placement nobody stops — a per-feature storage class, validation built inline in a handler, a file parser in the domain — passes every test and becomes the pattern the next feature copies. So the judgement step is written down, done by someone who did not write the plan, posted where everyone can see it, and checked before merge.

## 0. Read the project

- `AGENTS.md`, the conventions and placement table, decision records, and the stack conventions skill for every area the plan touches.
- The issue, the spec section, and the code the plan will change — check that the names, paths and APIs it relies on exist (or are clearly new).

## 1. Who reviews

- **Default:** spawn the `architect` agent (agents plugin) with a fresh context and only: the issue/spec link, the plan, and `AGENTS.md`. It must not see the conversation that produced the plan.
- No subagents in this tool? Do the review yourself in a separate, clearly labelled step, and say in the comment that it was not independent.
- It is **never** merged into the code review, shortened, or skipped to save time. Test reruns and review rounds may be trimmed for speed; this may not.

**Non-trivial = needs this review:** anything but a one-file change that adds no type, no file, no dependency and no rule. A typo, a wrong constant, a missing null check are trivial; a new class, endpoint, table, port, adapter, provider or background decision is not.

## 2. The questions, in order

The first three are answered in full, every time.

1. **Placement.** Which layer and file does each part land in — by the placement row of its kind (`engineering-principles` §3, the stack skill)? Anything that fits no row is a design question to resolve now, not a place to improvise.
2. **Reuse.** Does something already do this — a port, an adapter, a helper, a component, a provider, a shared rule? Name it, or say exactly what was searched (`grep` terms, the placement rows, the shared folders).
3. **The next feature.** Would the next feature of the same kind have to write this again (its own storage class, a second upload reader, a copied rule, a feature-specific variant of a generic port)? If yes, the generic piece is designed now and this feature builds on it.
4. **Patterns** and the problem each solves; anything speculative (YAGNI).
5. **Data:** tables, constraints, indexes, the migration path for released clients.
6. **Contract:** endpoints, error codes, compatibility with installed clients.
7. **Failure modes:** offline, retry, duplicate, race, crash mid-way; safety-critical paths named.
8. **Performance:** hot paths and their budgets; any call in a loop.
9. **Tests:** which seam proves each acceptance criterion; would any part fail the architecture tests (their baselines are empty — the plan must not need an entry)?

## 3. Output and posting

```markdown
## Design review — <YYYY-MM-DD>
Plan reviewed: <link or summary> · Reviewer: architect agent (independent) | author (not independent)

### Decisions
- <what the plan commits to> — because <reason>
### Reuse
- Use <existing piece> for <part>. / New shared piece: <name>, instead of a feature-specific one.
- Searched: <terms, folders>
### Risks (ranked)
- <risk> — scenario: <concrete failure> — fix: <change to the plan>
### Questions for the owner
### Costly-to-reverse choices
- <choice> → needs a decision record (`decision`, meta plugin)
### Open design findings
- [blocking] <finding> | None
```

Write it to a file in a **scratch directory outside the repository** (never a repository file), check it against the project's attribution policy, and post it as **one** comment on the issue from the table above (`gh issue comment <n> --body-file <file>`). Posting the required review on the project's own issue needs no extra OK; anywhere else, ask.

**Gate:** no open blocking design finding. The plan changes (and the review is updated) until there is none.

## 4. After the review

- The build follows the review's decisions; a deviation is explained in the PR.
- The code review's **design pass** (`code-review`, quality plugin) checks the diff against this review, and the `merge` skill (gate 5) checks it was posted before the first commit with production code.

## Rules

- Review the plan, not the author; findings need a scenario.
- Do not write code or edit repository files during the review; the review file lives in a scratch directory.
- A business rule nobody can find in the issue, spec or code is a question for the owner, never an assumption.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `start-issue`, `new-feature`, `bugfix`, `implement` | Posted `## Design review` | `implement`; checked by `code-review` (design pass) and `merge` |
