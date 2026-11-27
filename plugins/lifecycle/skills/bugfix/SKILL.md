---
name: bugfix
description: "Fix a bug end to end — reuse or run the investigation (reuse existing task context; preserve uncertainty when the cause is unverified), risk-appropriate design review, a permanent regression test that fails before for the reported reason and passes after, fix the root cause not the symptom plus the 'why was it breakable' guard, blast radius (same pattern, other platform, stored data repair, installed old versions), verify, then PR with the failure mode explained. Trigger on /bugfix, 'fix this bug', 'fix issue', 'make this test pass', 'implement the fix', 'hotfix'."
argument-hint: "[bug issue, investigation report path, or description]"
license: MIT
metadata:
  version: "2.0.0"
---

# Bugfix

Fix `$ARGUMENTS` (a bug issue, an investigation report, or a description). If empty, ask for the bug.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

`AGENTS.md`: commands, release paths, which paths are safety-critical, the merge gates.

## 1. Choose the entry

| You have | Do |
|---|---|
| An investigation report / root cause in this conversation | Use it; do not re-investigate |
| A bug issue with no root cause | `investigate-bug` first |
| Only a description | Reproduce with `investigate-bug`; use the current task as scope. File an issue only when policy or coordination requires it |
| An investigation that says not reproduced or unverified | Preserve uncertainty. Add discriminating instrumentation or characterization; an authorized reversible mitigation may proceed with monitoring and rollback. Do not claim a root-cause fix without evidence. |
| It is really a missing feature | `file-feature` instead |

**Safety-critical bug** (on the project's safety-critical list in `AGENTS.md`, or by default a critical action missed or duplicated, data exposed, lost or corrupted, a background worker dead): say so at the top of every reply; priority P0/P1; the PR needs `device-test` when platform code is involved.

## 2. Tier and design

Classify with `work-context` by impact, not file count. A fix that stays inside existing code is Standard: write the inline design check (where the fix lands, what existing guard it reuses, which test proves it). A fix that moves responsibilities, adds a shared piece for the bug class, changes a contract or stored data, is Structural: `design-review` before the fix. A fix on a declared high-risk area with no new structure gets the focused review (failure modes, tests, rollback) before the fix. The reproduction test may come first in both. A one-line access-control change is High-risk; a mechanical multi-file rename is Quick.

## 3. Branch

`start-issue` → a descriptive fix branch (include the issue number when one exists). If `investigate-bug` already created the linked branch with the reproduction test, keep using it.

## 4. Regression test (RED)

Make the reproduction a permanent test next to the related tests. It must fail on the code before the fix **for the reported reason** — read the failure message, not just "red". For platform-only bugs that cannot run in CI, add the closest test of the shared logic and write the device steps into the PR.

## 5. Fix the root cause

Change the deepest cause in our control (from supported causal evidence), not the symptom. Then the "why was this breakable" part, when small: a type, a guard at the boundary, a lint rule, an architecture test, an alert. Larger prevention work → its own issue.

Run the test → **GREEN**; then the area suite once.

**Gate:** red-before and green-after outputs are both captured.

## 6. Blast radius

- **Same pattern elsewhere:** `grep` for it; fix in this PR only if it is the same root cause, otherwise `file-bug`.
- **Other platform:** a fix on one platform's code usually needs the other checked.
- **Stored data:** a code fix does not repair wrong rows already stored. Write the repair (a migration or a reviewed one-off script) or file it as a follow-up; say which in the PR.
- **Installed old versions:** does the fix need a store release, or can it ship as a server change or an over-the-air patch (`release`)?

## 7. Verify

`implement` §3 in `bug` mode. Minimum: the regression test red-before/green-after (paste both), area suites green, device steps for platform bugs.

## 8. Review and PR

`pre-commit` (`fix(<scope>): …`), `create-pr`, and the review at the tier's depth (`code-review`: self-review for Quick, one independent review for Standard and above). The PR's safety/privacy notes explain the failure mode, who was affected, and how the test proves it cannot silently happen again. Then `ci`, `deploy-check` and `merge`. If the bug reveals a gap in a skill or convention, run `capture-lesson` (meta plugin).

## Rules

- No fix without a test that failed first (pure config/infra fixes: before/after evidence instead).
- Never weaken or delete an existing test to make the fix pass; if the test was wrong, say why in the PR.
- Never swallow the error that exposed the bug.
- Releases belong to the owner.

## Composition

| From | This skill | To |
|---|---|---|
| `investigate-bug`, `file-bug`, `incident` | Fixed, verified bug with a regression test | `pre-commit` → `create-pr` → `code-review` at the tier's depth → `ci` → `deploy-check` → `merge`; `release` when users need a build; `capture-lesson` |
