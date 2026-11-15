---
name: start-issue
description: "Start work on an issue — read it, its epic, spec and design; refuse a vague issue without acceptance criteria and tests to write first; create the branch from the issue so the tracker links it (never on main, never carrying unrelated work, never via a shared stash); write the plan; get the architect's design review posted on the issue before the first code commit; mark it in progress; then hand off to implement. Trigger on /start-issue, 'start issue', 'pick up issue', 'work on #', 'begin this ticket', 'set up a branch for'."
argument-hint: "[issue number or URL]"
license: MIT
metadata:
  version: "1.0.0"
---

# Start issue

Start work on issue `$ARGUMENTS` (number or URL). If empty, list open issues assigned to the user and ask which.

## 0. Read the project

`AGENTS.md`: tracker and repository, branch naming, worktree policy, which changes are non-trivial, the merge gates.

## 1. Read the context

```bash
gh issue view <n> --json number,title,body,labels,assignees,state,milestone
gh api repos/<owner>/<repo>/issues/<n>/parent --jq '"#\(.number) \(.title)"' 2>/dev/null || echo "no parent epic"
```

Then read what it links: the spec section, the investigation, the design frames (or the approved state table and flow), the epic's spec-level design review, related issues; for a bug, the investigation report.

**Spec merged first:** a feature slice starts only after its spec's docs PR is merged. If the owner wants to start earlier, pin the spec commit the slice was planned against (`git show <sha>:docs/specs/<NNN>-<slug>/spec.md`) and name it in the plan.

**Gate:** the issue is ready —
- a **feature** issue has acceptance criteria and "Tests to write first", and no open `needs-design`;
- a **bug** issue has the expected behaviour and "Regression test to add" (from `file-bug`);
- a **docs/chore** issue says what done looks like.

If not, stop: propose what is missing and ask the owner (or run `investigate-feature` / `investigate-bug`). Never start coding against a vague issue.

## 2. Branch

Name from the type and title: `feat/<n>-<slug>`, `fix/<n>-<slug>`, `chore/<n>-<slug>`, `docs/<n>-<slug>` (specs and other docs), where `<n>` is the issue number.

Check the checkout first: `git status --short`. Uncommitted or unpushed work that is not for this issue must not ride along — ask, then commit it on its own branch or use a separate worktree. Never stash: the stash is shared between worktrees and other sessions.

Create the branch **from the issue** so the tracker links it:

```bash
gh issue develop <n> --name feat/<n>-<slug> --base main
git fetch origin && git switch feat/<n>-<slug>
# or, when this checkout has other work in progress:
git worktree add ../<repo>-<n> feat/<n>-<slug>
gh issue develop --list <n>          # confirm the link
```

Already on a session branch? Push it, then create the linked branch on top of it (`--base "$(git branch --show-current)"`). Other trackers: name the branch with the issue key so the link is made. Never start on `main`.

## 3. Plan

Write a short plan (in the conversation; on the issue only if the owner wants it there):

- Files and folders to change, and the existing pattern to copy for each — by placement row (`engineering-principles` §3).
- Skills the work needs (`add-endpoint`, `add-migration`, `design-to-screen`, `background-work`, …) and companions (contract + regenerated clients, migrations, strings, bridges, docs).
- The test list in the order it will be written; the first one is the next action.
- Blocked? Label it (`blocked:<reason>`), comment `**Blocked by:** …`, tell the owner, pick the next issue.
- Device test needed?

## 4. Design review before code

For every feature slice and every non-trivial fix (anything but a one-file change that adds no type, file, dependency or rule), run `design-review`: the `architect` agent (agents plugin) reviews the plan and posts `## Design review — <date>` on **this issue** before the first commit with **production code**. A slice of a specified feature gets a short slice-level review that links the epic's spec-level review, but still answers placement, reuse and "would the next feature write this again?" for what the slice adds. A bug's reproduction test (or characterisation tests before a refactor) may be committed before the review; production code may not. Never skipped or shortened for speed. The plan changes until no design finding is open. A trivial fix says why it is trivial in its PR.

**Gate:** the design review comment is on the issue, or the change is trivial and says so.

## 5. Mark in progress

With the owner's OK when the issue is not already theirs:

```bash
gh issue edit <n> --add-assignee @me --add-label in-progress
```

First slice of a feature → set the spec's `status: in-progress`.

## 6. Hand off

Report: issue + epic, branch, plan, the design review link, the **first failing test to write**, key files. If the owner asked to build it (not only to set up), continue straight into `implement` in the matching mode (`feature`, `bug`, `maintenance`); docs issues go straight to writing, then `pre-commit` and `create-pr`.

## Rules

- One issue per branch and per PR.
- Read before planning; plan and design review before production code; a failing test before implementation.
- Labels and assignees change a shared board — only with the owner's OK.

## Composition

| From | This skill | To |
|---|---|---|
| `file-feature`, `feature-to-issues`, `file-bug`, `bugfix`, `new-feature` | Linked branch, plan, posted design review | `implement` |
