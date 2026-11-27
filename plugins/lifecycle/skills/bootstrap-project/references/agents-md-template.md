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
- Tracker: <GitHub Issues on owner/repo | other>. Use tracking for coordination or project policy; a direct authorized task suffices for a small change.
- Branches: `feat/<n>-<slug>`, `fix/<n>-<slug>`, `chore/<n>-<slug>`, `docs/<n>-<slug>`, include an issue number only when one exists.
- Commits: conventional (`feat(scope): …`). Author and attribution policy: <e.g. "commits authored by <account>; no AI co-author trailers">.
- Link relevant tracking; closing keywords only for fully resolved work.
- The step-by-step workflow and the skill for each step: docs/engineering-workflow.md.

## Design review and merge gates
- Tiers (`work-context`): **Quick** (copy, style, docs, config, test-only, a small reversible fix) → targeted checks and a self-review of the diff. **Standard** (behaviour inside existing structure) → short plan with the inline design check, test-first, one independent review at the end. **Structural / High-risk** (a feature or module from scratch, new layer/service, data model, contract, dependency, cross-cutting refactor, or a path listed below) → design review before code, failure-path tests, independent review with a full design pass.
- <Strict profile, only if the team wants it: "every change gets an issue and an independent review; every non-trivial change gets a design review before code".>
- Merge gates: <copy from the merge skill, adapted>. Who merges: <explicitly authorized actor once the gates hold>.
- Optional policies (delete what does not apply): <PR CI is off; run `make check` locally and paste the summary> · <area checks CI does not run: …> · <device tests are batched into one pass before release>.
- The speed rule: speed may cut test reruns, review rounds and ceremony the tier does not require — never the tests written, a Structural change's design review, or the design pass its tier requires.

## Safety-critical paths
<List: e.g. payment capture, sending critical notifications, the background sync.> **This list is the one the skills use**: their examples are only examples. Changes on these paths need failure-path tests, never swallow errors, and the PR explains the failure mode.

## Privacy rules
- <Personal data list.> Never logged at shipped levels, never sent to third-party analytics, never pasted into issues, PRs or test names.
- Sharing anything about a person is opt-in and visible to that person.

## Definition of done
1. Risk-appropriate verification passes; no artificial tests for prose-only edits.
2. Contract updated if the API changed; clients regenerated.
3. Screens match the design (states, copy, tokens).
4. PR says what changed and how it was tested, with real output.
5. Docs say what is true now.
```
