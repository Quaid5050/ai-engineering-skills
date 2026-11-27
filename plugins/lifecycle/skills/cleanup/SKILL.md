---
name: cleanup
description: "Tidy up after a pull request is merged or abandoned — confirm its state, close or update the issue and the epic checklist, delete the local and remote branch, remove the worktree from another checkout, and stop local services, emulators and dev servers started for the work, without touching other projects' containers or a shared stash. Use when a PR is merged or a branch is dead. Trigger on /cleanup, 'clean up', 'PR is merged, tidy up', 'remove the worktree', 'delete the branch', 'stop the services'."
argument-hint: "[PR or branch]"
license: MIT
metadata:
  version: "2.0.0"
---

# Cleanup

Tidy up after the work on `$ARGUMENTS` (a PR or branch; default the current branch).

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

From `AGENTS.md`: the tracker and its CLI, where worktrees live, how local services are started and stopped (the project's compose file or scripts), and whether the remote deletes merged branches automatically.

## 1. Confirm the state

```bash
gh pr view <PR|branch> --json number,state,mergedAt,headRefName,closingIssuesReferences
```

- **Merged** → continue.
- **Open** → stop; nothing to clean yet.
- **Closed without merge** → ask whether the work is abandoned before deleting anything: unmerged commits are lost with the branch.

**Gate:** the PR is merged, or the user confirmed the work is abandoned.

## 2. Issues

These change the shared board, so ask once for the batch:

- The issue closes automatically when the PR said `Closes #<issue>`; otherwise close it with a comment naming the PR.
- Remove workflow labels (in-progress).
- A sub-issue → check the epic's remaining sub-issues; when all are closed, tell the user the epic can close and the spec can be marked shipped.

## 3. Local git

```bash
git fetch --prune origin
git worktree list
```

- You cannot delete the branch checked out in the current worktree: leave it first (`git switch --detach origin/main`).
- `git branch -d <branch>` (refuses unmerged work). A squash-merged branch looks unmerged: confirm the PR is merged, then `-D` only with the user's OK.
- Remove a worktree **from another checkout**: `git -C <main checkout> worktree remove <path>` — it refuses when there are uncommitted changes; then ask.
- Remote branch: delete it only if the host did not (`git push origin --delete <branch>`), with the user's OK.
- **Never use `git stash`** in a repository shared by several worktrees or sessions: the stash is shared. Commit or discard instead, with the user's OK.

## 4. Local services

Stop what was started **for this work** and is no longer needed; ask first if unsure who started it:

- The project's local services (stop without deleting data volumes; deleting volumes only on request).
- Emulators/simulators started for the work, dev servers, background test runners from this session.
- **Never touch other projects' containers, services or volumes** on the same machine.

## Rules

- Nothing is deleted that is not merged without the user's OK.
- Never force-delete, prune volumes or reset branches others may use.

## Composition

| From | This skill | To |
|---|---|---|
| `merge` | A tidy machine and board | `start-issue` for the next issue |

## Report

What was closed, deleted and stopped, and anything left on purpose.
