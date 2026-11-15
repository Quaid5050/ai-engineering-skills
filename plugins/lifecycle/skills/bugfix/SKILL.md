---
name: bugfix
description: "Fix a bug end to end — reuse or run the investigation (no issue, no fix; unverified cause, no guessed fix), design review for a non-trivial fix, a permanent regression test that fails before for the reported reason and passes after, fix the root cause not the symptom plus the 'why was it breakable' guard, blast radius (same pattern, other platform, stored data repair, installed old versions), verify, then PR with the failure mode explained. Trigger on /bugfix, 'fix this bug', 'fix issue', 'make this test pass', 'implement the fix', 'hotfix'."
argument-hint: "[bug issue, investigation report path, or description]"
license: MIT
metadata:
  version: "1.0.0"
---

# Bugfix

Fix `$ARGUMENTS` (a bug issue, an investigation report, or a description). If empty, ask for the bug.

## 0. Read the project

`AGENTS.md`: commands, release paths, which paths are safety-critical, the merge gates.

## 1. Choose the entry

| You have | Do |
|---|---|
| An investigation report / root cause in this conversation | Use it; do not re-investigate |
| A bug issue with no root cause | `investigate-bug` first |
| Only a description | `file-bug` **first** (cause "unknown"), then `investigate-bug`, then update the issue. No issue, no fix |
| An investigation that says "not reproduced" or "unverified" | Stop. Report the missing evidence; never guess a fix |
| It is really a missing feature | `file-feature` instead |

**Safety-critical bug** (on the project's safety-critical list in `AGENTS.md`, or by default a critical action missed or duplicated, data exposed, lost or corrupted, a background worker dead): say so at the top of every reply; priority P0/P1; the PR needs `device-test` when platform code is involved.

## 2. Design review (non-trivial fixes)

A fix that adds a type, a file, a dependency or a rule, or touches more than one file of production code, is non-trivial: run `design-review` — where the fix lands, what it reuses, and whether the **same class of bug needs a shared fix** rather than a local patch. Posted on the bug issue before the first commit with production code (the reproduction test from `investigate-bug` may already be on the branch); never skipped for speed. A trivial one-line fix says why it is trivial in the PR.

## 3. Branch

`start-issue` → `fix/<n>-<slug>` from the issue. If `investigate-bug` already created the linked branch with the reproduction test, keep using it.

## 4. Regression test (RED)

Make the reproduction a permanent test next to the related tests. It must fail on the code before the fix **for the reported reason** — read the failure message, not just "red". For platform-only bugs that cannot run in CI, add the closest test of the shared logic and write the device steps into the PR.

## 5. Fix the root cause

Change the deepest cause in our control (from the five whys), not the symptom. Then the "why was this breakable" part, when small: a type, a guard at the boundary, a lint rule, an architecture test, an alert. Larger prevention work → its own issue.

Run the test → **GREEN**; then the whole area suite.

**Gate:** red-before and green-after outputs are both captured.

## 6. Blast radius

- **Same pattern elsewhere:** `grep` for it; fix in this PR only if it is the same root cause, otherwise `file-bug`.
- **Other platform:** a fix on one platform's code usually needs the other checked.
- **Stored data:** a code fix does not repair wrong rows already stored. Write the repair (a migration or a reviewed one-off script) or file it as a follow-up; say which in the PR.
- **Installed old versions:** does the fix need a store release, or can it ship as a server change or an over-the-air patch (`release`)?

## 7. Verify

`implement` §3 in `bug` mode. Minimum: the regression test red-before/green-after (paste both), area suites green, device steps for platform bugs.

## 8. Review and PR

`pre-commit` (`fix(<scope>): …`), `create-pr` (it opens the PR, then the reviewer agent posts the required code review). The PR's safety/privacy notes explain the failure mode, who was affected, and how the test proves it cannot silently happen again. Then `ci`, `deploy-check` and `merge`. If the bug reveals a gap in a skill or convention, run `capture-lesson` (meta plugin).

## Rules

- No fix without a test that failed first (pure config/infra fixes: before/after evidence instead).
- Never weaken or delete an existing test to make the fix pass; if the test was wrong, say why in the PR.
- Never swallow the error that exposed the bug.
- Releases belong to the owner.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-bug`, `file-bug`, `incident` | Fixed, verified bug with a regression test | `pre-commit` → `create-pr` → `code-review` (posted) → `ci` → `deploy-check` → `merge`; `release` when users need a build; `capture-lesson` |
