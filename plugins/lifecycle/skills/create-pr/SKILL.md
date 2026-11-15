---
name: create-pr
description: "Open a pull request the reviewer can trust — preconditions, reuse an existing PR, an issue gate (Closes #issue, the issue's labels and milestone), bring the branch up to date, collect real evidence first (command outputs, screenshots with synthetic data, the design review link, device tests listed as open), write a per-area description with safety and privacy notes, push and open on the user's go-ahead, then get an independent code review posted on the PR and fix critical and major findings before CI and merge. Use when the work on a branch is ready for review. Trigger on /create-pr, 'open a PR', 'create the pull request', 'push and open a PR', 'raise a PR', 'send this for review'."
argument-hint: "[branch | --draft | issue number]"
license: MIT
metadata:
  version: "1.0.0"
---

# Create PR

Open a PR for the current branch (or `$ARGUMENTS`: a branch, `--draft`, or an issue number to link).

## 0. Read the project

Read `AGENTS.md`, `CONTRIBUTING.md` and the PR template (`.github/pull_request_template.md` or the tracker's equivalent): the issue tracker and its CLI (default example: GitHub `gh`; use the project's tracker), labels and milestones, the base branch, the merge gates (`merge`), whether a push or PR needs the user's go-ahead, and the project's author/attribution policy for PR text.

## 1. Preconditions

```bash
git branch --show-current                 # not the main branch
git status --short                        # clean; otherwise run pre-commit first
git fetch origin && git log --oneline origin/main..HEAD
gh pr list --head "$(git branch --show-current)"     # reuse an existing PR
```

A PR already exists for the branch → update it (push + edit) instead of opening another.

**Issue gate:** the PR must close an issue. Find it from the branch name or search the tracker. No issue → stop and create one (`file-feature`, `file-bug`) before opening the PR. The PR body starts with `Closes #<issue>` (one line per issue it closes) and the PR gets the issue's labels (minus workflow labels such as in-progress/blocked) and milestone, plus an area label for every area the diff touches.

## 2. Bring it up to date

```bash
git rebase origin/main          # or: git merge origin/main once the branch was pushed and reviewed
```

Conflicts → resolve, re-run the affected `pre-commit` checks. Never force-push the main branch; on a feature branch use `--force-with-lease`, and only with the user's OK. Check every commit's author and message against the project's policy: `git log --format='%an <%ae> %s' origin/main..HEAD`.

## 3. Evidence before the description

Collect real results — never "tests pass" without output:

- Lint/analyze/test/build output per changed area (counts).
- Screenshots of changed screens, synthetic data only.
- A link to the issue's design review comment (feature or non-trivial fix, `design-review`) and how the diff follows it.
- Device tests (`device-test`, mobile plugin) for changes to background work, notifications, widgets or battery; not done yet → list them as **open** (some projects batch them into one pass before release — their policy in `AGENTS.md`).
- Performance numbers (`perf-check`, quality plugin) when a budget applies.

**Gate:** every claim the description will make has its evidence in hand.

## 4. Write the description

Follow the project's template; when it has none, use this. In a repository with several areas the reader must see per area what changed and **why** without opening the diff.

```markdown
## Brief
Closes #<issue>

<1–2 lines: what changed for the user and why.>

## Areas changed
- [x] **Backend** · 7 files — validation for order lines moved into the domain so every entry point shares it.
- [x] **Web client** · 4 files — the order form shows the server's limit error.
- [ ] **Mobile client**
- [ ] **Infrastructure / CI**
- [ ] **Docs**

## Acceptance criteria
- [x] <criterion from the issue> — how it was checked
- [ ] <criterion not met yet> — why (draft only)

## How it was tested
- [x] `<test command>`: 132 passed
- [ ] Not tested: <what and why>

## Design review
<link to the issue's design review> — followed / deviations and why

## Code review
- [ ] Posted and covering the head commit; no open critical or major

## Safety / privacy notes
Failure modes considered (offline, retry, duplicate, crash mid-way, permission revoked…) and the test for each. What personal data moves where. "None" only if nothing safety- or privacy-relevant changed.

## Screenshots
Before / after, synthetic data.
```

Keep the unticked areas: they show what was *not* touched. Update the list when later commits touch new areas. Plain prose, no filler. Follow the project's attribution policy; if it forbids AI mentions, grep the body file before using it: `grep -niE 'co-authored-by|generated with' <body-file>` must print nothing.

## 5. Push and open

**Go-ahead first:** pushing and opening a PR are visible to others. Show the title, labels and description and get the user's OK, unless their request already said to open the PR.

```bash
git push -u origin HEAD
gh pr create --base main --head "$(git branch --show-current)" \
  --title "<conventional title>" --body-file <body-file> \
  --label "<issue labels>" --milestone "<issue milestone>" [--draft]
```

Write the body to a file first (a scratch directory), never inline in the command.

## 6. Code review (required before merge)

The review happens **after** the PR is open, so it can be posted where everyone sees it, and it has **one** posting owner: the reviewer.

1. Spawn the **`reviewer` agent** (agents plugin) with only the PR link — fresh context, no access to the conversation that wrote the code. It runs `code-review` (quality plugin), runs `security-privacy-review` when the change touches personal data, auth, sharing, uploads, payments or analytics and posts it as its own `## Security & privacy review — <SHA>` comment, and **posts** the review itself as one comment starting `## Code review — <short head SHA>`. If it cannot post (no tracker access in that tool), it returns the text and you post it unchanged.
2. You do not write or post a second review; you only **verify** the comment exists and names the current head SHA.
3. Fix every `critical` and `major` finding (or record the user's explicit decision to defer it in the PR), push, and post `## Code review — <new SHA> (re-review)` covering only the new commits against the open findings.
   The re-review is again run and posted by a fresh `reviewer` agent.
4. `minor`/`nit`: fix or answer them in the re-review.

**Gate:** the latest review covers the head commit with no open critical/major and no open major in its design pass.

## 7. Watch CI

Hand off to `ci` (ship mode), then `deploy-check` where it applies (the change touches API, data, platform code, config or scheduling; its verdict is posted on the PR — merge gate 8), then `merge` when its gates hold. Do not request human reviewers unless the project's policy says to.

## Rules

- One issue per branch and PR; no unrelated changes ride along.
- Never claim a check you did not run; keep implemented, verified, PR open, CI green, merged and released distinct.
- The author never reviews its own change as the independent review.
- A force-push or pushing to someone else's branch needs its own OK.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `bugfix`, `pre-commit` | PR opened, then the independent review posted on it | `ci` → `deploy-check` → `device-test` (mobile; before merge unless the project batches it) → `merge` → `release` |
| `reviewer` agent, `code-review`, `security-privacy-review` (quality) | The review posted on the PR | fixes → re-review |

## Report

PR link, CI state per job, review verdict and risk tier with a link to the review comment, what is still open (device test, findings), and whether it was merged or why not.
