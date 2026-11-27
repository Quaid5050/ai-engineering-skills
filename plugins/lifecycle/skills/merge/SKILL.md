---
name: merge
description: "Check a PR's merge gates for the exact head commit at its risk tier — CI on the head against current main, a review covering the head, the issue link, area checks CI skips, the design review for structural work, the design pass, the merging session's own read of the diff, required security and deploy verdicts — then merge only when the project's policy allows. Explicit no-merge instructions always stop before merging. Trigger on /merge, 'merge this', 'is this ready to merge', 'check the gates', 'merge the stack'."
argument-hint: "[PR]"
license: MIT
metadata:
  version: "2.0.0"
---

# Merge

Check the gates for `$ARGUMENTS` (a PR; default the current branch's PR) and merge when they hold and the policy allows. If not ready, say exactly which gate fails and what fixes it. Eligibility is not authorization; a user's no-merge instruction always wins.

## 0. Read the project

Reuse the task card and tier from `work-context` (foundation plugin). From the project's agent rules read:

- **The merge policy:** may the agent merge once the gates hold, or must it ask? **Default: ask.** Follow exactly what the project says.
- The merge method, required check names, area checks CI does not run, and the project's extra gates. Project gates add to the ones below; they never remove one.
- **Optional project policies**, only if stated: PR CI off with local checks standing in; area checks that run only on main; device tests batched into one pass before release; agent merges without asking.

Never assume the default branch is called main.

## 1. The gates

A PR is ready only when every gate that applies to its tier holds:

| # | Gate | Quick | Standard | Structural / High-risk |
|---|---|---|---|---|
| 1 | Required CI green **on the head commit, against current main** (a PR behind main merges main in and gets a fresh run; PR CI off → the project's full local check on the head, summary in the PR) | ✓ | ✓ | ✓ |
| 2 | A review covering the head with no open `critical`/`major` (`code-review`); later commits are reviewed fixes or get a delta re-review | self-review | independent | independent |
| 3 | The PR links its task (`Closes #<issue>` when the change completes it; a partial change only references it) | if the project tracks issues | ✓ | ✓ |
| 4 | Area checks CI does not run, run locally on the head with output in the PR | if touched | if touched | if touched |
| 5 | Design review before production code (`design-review`), no open blocking finding | — | inline design check in the plan | ✓ separate; independent when a subagent or second person is available, otherwise a labelled self-review (a project may require independence) |
| 6 | The design pass has no open `major` | — | ✓ on the diff | ✓ against the design review |
| 7 | **The merging session has read the diff itself** (`gh pr diff <PR>`): it does what the task says, nothing more, and follows the design | ✓ | ✓ | ✓ |
| 8 | Required verdicts: `deploy-check` when API, data, platform code, configuration or scheduling changed; `security-privacy-review` when personal data, auth, sharing, uploads, payments or analytics changed; nothing unsafe open unless the owner's acceptance is quoted | if touched | if touched | if touched (always for a declared high-risk area) |

Review and check evidence must come from a trusted identity and cover the candidate; a comment title, an author-controlled timestamp or a copied summary is not proof, and a later code change invalidates it.

**The speed rule:** speed may cut test **reruns**, review **rounds** and ceremony the tier does not require. It never cuts the tests written, the design review a Structural change needs, or the design pass its tier requires.

Commands are in [references/commands.md](references/commands.md).

**Gate:** each applicable gate is ticked with evidence (a link, a SHA, a command output); each inapplicable one says why. A failing gate is fixed, never bypassed.

## 2. Merge

1. Policy says ask, or the user has not authorized merging → show the ticked gates and ask. Policy allows → merge.
2. Use the expected-head merge (or the merge queue) so a changed head cannot merge under stale evidence: `gh pr merge <PR> --merge --match-head-commit <sha>` (or the project's method).
3. Close the issue only if this change fulfils it; update the epic checklist.
4. **Watch main's CI** after the merge. A red main is fixed before anything else merges.

**Stacked PRs** and **batched device tests**: see [references/commands.md](references/commands.md).

## Rules

- No admin merge, no disabled check, no "review later".
- Never merge someone else's PR or a fork's PR without the user's OK.
- Merging is not releasing; releases and deploys keep their own approvals (`release`).
- Report precisely: implemented, verified, PR open, CI green, merged, released are six different states.

## Composition

| From | This skill | To |
|---|---|---|
| `ci` (green), `code-review` (covers head), `deploy-check` / `security-privacy-review` (verdicts), `design-review` (Structural) | Gates checked; merged when allowed | `release`, `cleanup` |
