# lifecycle 1.0.0

The whole delivery lifecycle as gated skills: idea, MVP scope, project bootstrap, feature investigation, spec, issues, design review before code, test-first implementation, pre-commit, PR, CI, deploy check, merge gates, release, observe, incident, postmortem, cleanup. Framework-agnostic.

## Install

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install lifecycle@ai-engineering-skills
```

Installs with: `quality`, `agents`.

## Skills

| Skill | What it does |
|---|---|
| [`bootstrap-project`](skills/bootstrap-project/SKILL.md) | New repo (or one with no rules): stack decisions, walking skeleton, `AGENTS.md`, placement table + architecture tests, CI on hosted runners, labels and milestones |
| [`bugfix`](skills/bugfix/SKILL.md) | Regression test red → root-cause fix → green; blast radius and data repair |
| [`ci`](skills/ci/SKILL.md) | Drive CI to green, debug failures, optimise, change workflows safely (hosted runners for public repos) |
| [`cleanup`](skills/cleanup/SKILL.md) | After merge: issues, branches, worktrees, local services |
| [`create-pr`](skills/create-pr/SKILL.md) | Open a PR with real evidence, per-area summary, safety notes; independent code review posted |
| [`deploy-check`](skills/deploy-check/SKILL.md) | Before merge: what breaks users after deploy — contract, migrations, native changes, config, rollback |
| [`design-review`](skills/design-review/SKILL.md) | The mandatory review of a plan before code: placement, reuse, "would the next feature write this again?" |
| [`engineering-principles`](skills/engineering-principles/SKILL.md) | Where code goes and why: layers, the concept test, ports, placement rows, patterns, allowlist tests |
| [`feature-to-issues`](skills/feature-to-issues/SKILL.md) | Approved spec → epic + vertical-slice sub-issues, riskiest first |
| [`file-bug`](skills/file-bug/SKILL.md) | Record a bug: observed vs expected, repro, severity → priority, regression test to add |
| [`file-feature`](skills/file-feature/SKILL.md) | One scoped slice → an issue with criteria and tests to write first |
| [`implement`](skills/implement/SKILL.md) | The build-and-verify contract for features, fixes and maintenance; evidence per change type |
| [`incident`](skills/incident/SKILL.md) | Live problem: severity, mitigate first, timeline, communicate, recover |
| [`investigate-bug`](skills/investigate-bug/SKILL.md) | Reproduce first, five hypotheses, five whys, blast radius, "prevent the class" |
| [`investigate-feature`](skills/investigate-feature/SKILL.md) | Before specifying: design, scope, existing code, states, data, safety, privacy → build pack |
| [`merge`](skills/merge/SKILL.md) | The eight merge gates, the speed rule, merging, watching main |
| [`new-feature`](skills/new-feature/SKILL.md) | Build one feature end to end; routes through every step below with gates |
| [`observe`](skills/observe/SKILL.md) | Answer a production health question, or add errors/metrics/alerts for a change |
| [`postmortem`](skills/postmortem/SKILL.md) | Blameless write-up; which rung caught it and which should have; follow-ups |
| [`pre-commit`](skills/pre-commit/SKILL.md) | Before every commit: branch, staged paths, secrets, generated code, checks, conventional message |
| [`release`](skills/release/SKILL.md) | Choose the release path, staged rollout with approvals, watch, roll back |
| [`shape-idea`](skills/shape-idea/SKILL.md) | A raw idea → product brief, riskiest assumptions, MVP scope in milestones |
| [`spec`](skills/spec/SKILL.md) | Multi-area, schema, safety-critical or privacy work: requirements with acceptance criteria, failure modes, rollout; fresh-agent review + design review before approval |
| [`start-issue`](skills/start-issue/SKILL.md) | Branch from the issue, plan, design review posted before code |

See the [catalogue](../../README.md#catalogue) and the [workflow map](../../docs/engineering-workflow.md). License: MIT.
