---
name: merge
description: "The one definition of the merge gates, and merging once they hold — required CI green on a head commit that contains current main, a posted code review covering that head with no open critical or major finding, the PR closing its issue, area checks CI does not run pasted from a local run, a design review posted before the first production-code commit for any feature or non-trivial fix, a design pass with no open major, the merging session reading the diff itself, and the deploy-check and security-privacy verdicts posted where they apply. Stacked PRs bottom-up; a red main is fixed first. Speed may cut test reruns and review rounds, never the tests written, the design review or the design pass. Use when a PR looks ready. Trigger on /merge, 'merge this', 'is this ready to merge', 'can I merge', 'merge gates', 'ship the PR'."
argument-hint: "[PR]"
license: MIT
metadata:
  version: "1.0.0"
---

# Merge

Check the merge gates for `$ARGUMENTS` (a PR; default the current branch's PR) and merge when they hold. If it is not ready, say exactly which gate fails and what fixes it.

## 0. Read the project

From `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md`:

- **The merge policy:** may the agent merge itself once the gates hold, or must it ask? **Default: ask.** Some projects let the agent merge every PR whose gates hold, including high-risk ones; follow exactly what the project says.
- The merge method (merge commit, squash, rebase), the required check names, area checks CI does not run, and any extra gates the project adds. Project gates add to the eight below; they never remove one.
- **Optional project policies** (only if `AGENTS.md` states them): PR CI is switched off and local checks stand in for it; some area checks run only on main and must be run locally; device tests are batched into one real-device pass before release; the agent merges without asking. Without such a statement, none of them applies.

## 1. The gates

A PR is ready only when **all** of these hold:

1. **CI green on the head commit, against current main.** Every required check is green, or skipped because its area did not change. A PR that is behind main (or was just retargeted) merges main in, pushes, and gets a fresh green run. If the project's policy says PR CI is off, this gate is the project's full local check run on the head commit with its summary pasted in the PR.
2. **A posted code review covering the head commit** (`code-review`, quality plugin, run by the `reviewer` agent, agents plugin), with no open `critical` or `major` finding. Commits after the reviewed one are only reviewed fixes, or get a re-review note.
3. **The PR closes its issue** (`Closes #<issue>` in the body).
4. **Area checks CI does not run** (only if the project lists any), run locally on the head commit with their output in the PR.
5. **Design review before production code.** For a feature or a non-trivial fix (`engineering-principles` §5), the slice or bug issue has a design review (`design-review`) posted **before the first commit with production code** — a reproduction test or characterisation tests may come first — and no design finding is open. For a slice of a specified feature, the epic's spec-level review exists too.
6. **The design pass** of the code review has no open `major` finding.
7. **The merging session has read the diff itself.** Green tests and a positive review are not enough: read `gh pr diff <PR>` and confirm it does what the issue says, nothing more, and follows the design review.
8. **Required verdicts are posted.** `deploy-check` when the change touches the API, data, platform code, configuration or scheduling; `security-privacy-review` (quality plugin) when it touches personal data, auth, sharing, uploads, payments or analytics. No unsafe deploy-check row and no critical privacy finding is open, unless the owner's acceptance is quoted in the PR.

**The speed rule:** speed may reduce test **reruns** and review **rounds**. It never reduces the tests written, the design review, or the design pass.

```bash
gh pr view <PR> --json headRefOid,mergeStateStatus,statusCheckRollup,body,closingIssuesReferences
gh pr view <PR> --comments          # the newest "## Code review — <SHA>" must cover the head
gh issue view <issue> --comments    # the "## Design review — <date>" and its timestamp vs the first production-code commit
gh pr diff <PR>                     # gate 7
```

**Gate:** each of the eight is ticked with its evidence (a link, a SHA, a command output). One failing gate → fix it, never bypass it.

## 2. Merge

1. Policy says ask → show the ticked gates and ask. Policy allows the agent to merge → merge without asking.
2. `gh pr merge <PR> --merge` (or the project's method).
3. Confirm the issue closed; update the epic's checklist if there is one.
4. **Watch main's CI** after the merge. A red main is fixed before anything else merges.

**Stacked PRs:** merge bottom-up. After the bottom one merges, retarget the next to main (`gh pr edit <next> --base main`), merge main in, wait for a fresh green run and a review that covers the new head, then merge.

**Open device tests** do not hold a merge only when the project's policy batches them into one real-device pass before release; list them in the PR as open and run `device-test` (mobile plugin) before `release`. Otherwise they are part of gate 4.

## Rules

- A failing gate is fixed, never bypassed: no admin merge, no disabled check, no "review later".
- Never merge someone else's PR, or a PR from a fork, without the user's OK.
- Releases and deploys keep their own approvals (`release`); merging is not releasing.
- Report states precisely: implemented, verified, PR open, CI green, merged, released are six different things.

## Composition

| From | This skill | To |
|---|---|---|
| `ci` (green), `create-pr` (review posted), `deploy-check` (verdict) | Gates checked, merged | `release`, `cleanup` |
| `design-review` | Gate 5 evidence | — |
| `deploy-check`, `security-privacy-review` (quality) | Gate 8 verdicts | — |

## Report

Each gate → evidence; the merge commit; main's CI state after the merge; anything left open (device tests, follow-up issues).
