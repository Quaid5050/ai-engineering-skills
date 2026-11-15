# AGENTS.md template

Fill every `<…>` with a real value. Run every command before writing it down. Delete a section only if it truly does not apply.

```markdown
# Agent rules (any coding agent)

## Project
<Product in one paragraph: who it is for, what it does. What is personal data here.>

## Layout
- `<server>/` — <stack>. Layers: <edge> → <application> → <domain>; <persistence>; <adapters>. See docs/conventions.md.
- `<client>/` — <stack: web app, mobile app, or both>. Layout per the stack's conventions (`web-conventions` / `mobile-conventions`), e.g. `<features>/<feature>/...`; shared code in `<shared>/` with its rules in docs/conventions.md.
- `contracts/<api>.yaml` — the API contract. Change it first, then the server, then regenerate clients.
- Built vs planned: <table or list>. Describe only what exists as fact; mark the rest "planned".

## Commands
| Task | Command |
|---|---|
| Start local services | `<cmd>` |
| Server build + all tests | `<cmd>` |
| One server test | `<cmd with filter>` |
| Client analyze + all tests | `<cmd>` |
| One client test | `<cmd>` |
| Format / lint | `<cmd>` |
| Regenerate API client | `<cmd>` |
| Everything CI runs | `make check` |

## Workflow
- Tracker: <GitHub Issues on owner/repo | other>. No work without an issue; an epic with sub-issues for multi-slice work; milestones `A — …`.
- Branches: `feat/<n>-<slug>`, `fix/<n>-<slug>`, `chore/<n>-<slug>`, `docs/<n>-<slug>`, created from the issue.
- Commits: conventional (`feat(scope): …`). Author and attribution policy: <e.g. "commits authored by <account>; no AI co-author trailers">.
- PR body says `Closes #<issue>` and carries the issue's labels and milestone.
- The step-by-step workflow and the skill for each step: docs/engineering-workflow.md.

## Design review and merge gates
- Every feature and non-trivial fix: an architect design review of the plan, posted before the first commit with production code (spec-level on the epic, per slice on the slice issue).
- Every PR: a code review with a separate design pass, posted on the PR.
- Merge gates: <copy from the merge skill, adapted>. Who merges: <the agent once the gates hold | a human>.
- Optional policies (delete what does not apply): <PR CI is off; run `make check` locally and paste the summary> · <area checks CI does not run: …> · <device tests are batched into one pass before release>.
- The speed rule: speed may reduce test reruns and review rounds, never the tests written, the design review or the design pass.

## Safety-critical paths
<List: e.g. payment capture, sending critical notifications, the background sync.> **This list is the one the skills use**: their examples are only examples. Changes on these paths need failure-path tests, never swallow errors, and the PR explains the failure mode.

## Privacy rules
- <Personal data list.> Never logged at shipped levels, never sent to third-party analytics, never pasted into issues, PRs or test names.
- Sharing anything about a person is opt-in and visible to that person.

## Definition of done
1. Tests written first and passing; lint clean.
2. Contract updated if the API changed; clients regenerated.
3. Screens match the design (states, copy, tokens).
4. PR says what changed and how it was tested, with real output.
5. Docs say what is true now.
```
