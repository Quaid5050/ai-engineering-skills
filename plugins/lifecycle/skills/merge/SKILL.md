---
name: merge
description: "Check exact-candidate merge eligibility and merge only when authorized. Use when asked to assess readiness or merge a PR; explicit no-merge instructions always stop before mutation."
argument-hint: "[PR]"
license: MIT
metadata:
  version: "2.0.0"
---

# Merge eligibility and authorized merge

Assess `$ARGUMENTS` against the project's gates. Eligibility is not authorization. An explicit user instruction not to merge takes precedence over automatic merge policy.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

Read the current candidate, target branch, required checks, review rules, merge method and user authorization. Reuse the risk tier from `work-context`. Never assume the default branch is named main.

## 1. Verify eligibility for the exact candidate

1. Read the complete diff and linked acceptance criteria; include interactions with earlier changes when re-reviewing fixes.
2. Required checks pass for the actual candidate and relevant base/merge-group state. Skips need a verified unaffected area, not a missing check. A project's explicitly documented alternative evidence is recorded as such.
3. Required review is from a trusted reviewer/check identity and covers the candidate. A comment title, author-controlled timestamp or copied summary is not proof. Later code changes invalidate applicable review/check evidence.
4. Design assessment matches the risk tier: separate pre-change review for high-risk work where required; focused design consideration for standard work; no invented architect gate for quick work.
5. Applicable security and deployment-readiness assessments are complete, with no unresolved blocking risk. Actual deployment remains separately authorized.
6. Required local/device/manual evidence is recorded, or explicitly pending under an allowed project policy. Never label pending as passed.
7. Link the relevant task. Close an issue only if this change fulfills it; an audit or partial remediation can relate to a tracking issue without closing it.

Report each applicable gate with source revision, environment, trusted evidence and result. Inapplicable checks have a reason. Resolve failures rather than bypassing protected-branch controls.

## 2. Act only if authorized

If merging is prohibited or not requested/authorized, stop at the eligibility report. Otherwise use the platform's expected-head compare-and-merge control or merge queue so a changed head cannot be merged under stale evidence. Do not force administrative bypasses.

After an authorized merge, confirm the resulting state and relevant target-branch CI. Issue closure, release and deployment each follow their own scope; merging alone does not authorize a release.

## Rules

- Never merge on the basis of forged/stale comments or tests from a different snapshot.
- Never override an explicit no-merge instruction.
- Distinguish ready, merged and released in the result.

## Composition

| From | This skill | To |
|---|---|---|
| Reviewed candidate and applicable checks | Eligibility report; merge only when authorized | `release` or `cleanup` only within their own authorization |
