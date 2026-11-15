# AI Engineering Skills

A framework-agnostic skills and agents marketplace for the **whole engineering lifecycle with AI coding agents** — from a raw idea to a product in users' hands, and back again when something breaks. Backend, mobile app and web. Any stack.

It installs as a **Claude Code plugin marketplace**, and every skill is a plain [Agent Skills](https://agentskills.io/specification) `SKILL.md`, so Codex, Cursor, Gemini CLI, GitHub Copilot and other agents can use them too.

## Why this exists

Coding agents follow written rules and copy the code next to them. They are fast, and they are confidently wrong in exactly the places nobody wrote down. These skills are the written-down part: each one is a workflow that was hardened by real failures — audits, bugs that passed every test, reviews that missed things — and each lesson became a gate, a check or a rule. The ideas that matter most:

- **Design review before code.** Every feature and non-trivial fix gets an independent architect review of its *plan*, posted on the issue before the first code commit: where each part lands, what already exists to reuse, and *would the next feature have to write this again?*
- **A separate design pass in every code review.** Not bugs — placement, duplication across features, reuse. A wrong placement the next feature would copy is a `major` finding.
- **One home per technical kind of code.** Secrets per purpose, one storage port, one upload reader, rate limiters, background loops, shared code — each with a stated home and a test. A `utils` folder is not bad; a folder with no rules is.
- **Allowlist architecture tests with empty baselines.** Denylists ("the domain doesn't use the ORM") pass every kind of code nobody thought of. Allowlists don't. No exceptions by precedent.
- **Test-first, failure paths first** on anything where a silent failure harms a person or loses money or data.
- **Merge gates** including "the merging agent reads the diff itself" — and **the speed rule**: going faster may cut test reruns and review rounds, never the tests written, the design review or the design pass.
- **The project wins.** Every skill first reads the target project's own `AGENTS.md`, conventions and stack, and adapts. Stack detail lives in optional `references/<stack>.md` files, never in the core text.

## Install

### Claude Code

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install lifecycle@ai-engineering-skills
```

`lifecycle` pulls in `quality` and `agents` as dependencies. Add the area plugins you need:

```text
/plugin install backend@ai-engineering-skills
/plugin install mobile@ai-engineering-skills
/plugin install web@ai-engineering-skills
/plugin install meta@ai-engineering-skills
/plugin install guardrails@ai-engineering-skills     # opt-in hooks: secret scan, no commits on main
```

From a shell (CI, scripts):

```bash
claude plugin marketplace add Quaid5050/ai-engineering-skills
claude plugin install lifecycle@ai-engineering-skills
```

Skills are namespaced by plugin: `/lifecycle:new-feature`, `/quality:code-review`, `/backend:add-endpoint`. Agents: `agents:architect`, `agents:reviewer`, `agents:tester`. Agents also pick skills automatically from their descriptions.

Update later with `/plugin marketplace update ai-engineering-skills`.

### Other agents (Codex, Cursor, Gemini CLI, Copilot, …)

The skills are standard `SKILL.md` folders. Copy or link them into the folder your agent reads:

```bash
git clone https://github.com/Quaid5050/ai-engineering-skills
cd ai-engineering-skills
scripts/install-skills.sh /path/to/your-project/.agents/skills          # copy all skills
scripts/install-skills.sh ~/.codex/skills --link                         # or link, to stay in sync
scripts/install-skills.sh .cursor/skills --plugins lifecycle,quality,backend
```

Common locations (check your tool's current docs — they change): `.agents/skills/` (a shared location many agents read), `.codex/skills/` or `~/.codex/skills/` (Codex), `.cursor/skills/` (Cursor), `.gemini/skills/` (Gemini CLI), `.github/skills/` (GitHub Copilot). The three review agents are plain Markdown role descriptions; [docs/other-agents.md](docs/other-agents.md) shows how to use them where an agent has no subagents.

## Start here

| You have | Run |
|---|---|
| An idea and no repository | `shape-idea` → `bootstrap-project` → `new-feature` |
| A repository with no agent rules | `bootstrap-project` (it adds `AGENTS.md`, the placement table, architecture tests, CI) |
| A feature to build | `new-feature` (it chains everything below) |
| A bug | `file-bug` → `investigate-bug` → `bugfix` |
| Production is broken | `incident` → `postmortem` → `capture-lesson` |

The full lifecycle map, with which skill runs at each step: [docs/engineering-workflow.md](docs/engineering-workflow.md).

## Catalogue

### `lifecycle` — idea to production

| Skill | When to use |
|---|---|
| `shape-idea` | A raw idea → product brief, riskiest assumptions, MVP scope in milestones |
| `bootstrap-project` | New repo (or one with no rules): stack decisions, walking skeleton, `AGENTS.md`, placement table + architecture tests, CI on hosted runners, labels and milestones |
| `new-feature` | Build one feature end to end; routes through every step below with gates |
| `investigate-feature` | Before specifying: design, scope, existing code, states, data, safety, privacy → build pack |
| `spec` | Multi-area, schema, safety-critical or privacy work: requirements with acceptance criteria, failure modes, rollout; fresh-agent review + design review before approval |
| `feature-to-issues` | Approved spec → epic + vertical-slice sub-issues, riskiest first |
| `file-feature` | One scoped slice → an issue with criteria and tests to write first |
| `file-bug` | Record a bug: observed vs expected, repro, severity → priority, regression test to add |
| `start-issue` | Branch from the issue, plan, design review posted before code |
| `design-review` | The mandatory review of a plan before code: placement, reuse, "would the next feature write this again?" |
| `implement` | The build-and-verify contract for features, fixes and maintenance; evidence per change type |
| `investigate-bug` | Reproduce first, five hypotheses, five whys, blast radius, "prevent the class" |
| `bugfix` | Regression test red → root-cause fix → green; blast radius and data repair |
| `pre-commit` | Before every commit: branch, staged paths, secrets, generated code, checks, conventional message |
| `create-pr` | Open a PR with real evidence, per-area summary, safety notes; independent code review posted |
| `ci` | Drive CI to green, debug failures, optimise, change workflows safely (hosted runners for public repos) |
| `deploy-check` | Before merge: what breaks users after deploy — contract, migrations, native changes, config, rollback |
| `merge` | The eight merge gates, the speed rule, merging, watching main |
| `release` | Choose the release path, staged rollout with approvals, watch, roll back |
| `observe` | Answer a production health question, or add errors/metrics/alerts for a change |
| `incident` | Live problem: severity, mitigate first, timeline, communicate, recover |
| `postmortem` | Blameless write-up; which rung caught it and which should have; follow-ups |
| `cleanup` | After merge: issues, branches, worktrees, local services |
| `engineering-principles` | Where code goes and why: layers, the concept test, ports, placement rows, patterns, allowlist tests |

### `quality` — tests, review, security, accessibility, performance

| Skill | When to use |
|---|---|
| `testing-doctrine` | The rules every test follows: exact, hard-coded, fakes only at real boundaries, failure paths first, prove it can fail |
| `tdd` | Red-green-refactor, one behaviour at a time |
| `write-tests` | Write tests for code or a diff at the right level (stack references: .NET, Python, Node, JVM, Flutter, Swift) |
| `code-review` | Review a diff or PR: dimensions + the separate design pass + risk tier, posted on the PR |
| `security-privacy-review` | Data flow, authorisation and isolation, consent, abuse cases, the logging rule, OWASP API pass, retention |
| `accessibility-audit` | WCAG 2.2 AA for web and mobile: automated checks, screen readers, text scaling, contrast |
| `perf-check` | Measure against a budget, profile, change one thing, guard it (backend, web, mobile references) |
| `analytics-event` | Add a privacy-safe product event, or answer a product question from events |

### `backend`

| Skill | When to use |
|---|---|
| `backend-conventions` | Structure server code: layers, thin edges, validation, errors, transactions, resilience, data integrity, architecture tests (.NET, Django, Node, Spring references) |
| `add-endpoint` | Contract-first endpoint with forbidden-caller tests and regenerated clients |
| `add-migration` | Schema change: expand → migrate → contract, read the SQL for locks and rewrites |
| `add-scheduled-job` | Server jobs and outbound notifications: one scheduler, claimed rows, a unique sent-ledger, access re-checked at run time, zone-aware schedules |
| `add-file-upload` | Uploads and attachments: one upload reader + storage port, type from bytes, size caps, metadata stripped, complete only when all files arrive |
| `data-check` | Read-only, privacy-safe database questions and migration verification |

### `mobile`

| Skill | When to use |
|---|---|
| `mobile-conventions` | App architecture (view → view model → repository → service), shared code with rules, permissions UX, offline storage, performance (Flutter, React Native, Kotlin, Swift references) |
| `shared-core` | One functional core shared by Android and iOS, thin platform shells, interop rules (Kotlin Multiplatform reference) |
| `background-work` | Anything that runs while the app is closed: OS mechanisms, battery, app killers, every stop reported |
| `offline-queue` | A durable on-device outbox that never loses a record silently |
| `design-to-screen` | Build a screen from a design: inventory, tokens, every state, tests first, screenshot comparison |
| `home-widget` | Home/lock-screen widgets, live activities, tiles: all states, precomputed snapshot, privacy |
| `device-test` | Real-device checklist (low-end Android, recent Android, iPhone) recorded in the PR |

### `web`

| Skill | When to use |
|---|---|
| `web-conventions` | Structure a web front end — content sites and web apps: thin routes, components, tokens, server-state cache, auth and errors, zero-JS by default for content, CSP, privacy (React/Next.js, Astro references) |
| `build-web-screen` | An app screen: data fetching, forms, auth/session, 401/403/404 handling, every state, tests first; a no-design wireframe path |
| `add-web-page` | A content page or section, test-first, with accessibility, performance and CSP checks |

### `agents`

| Agent | When to use |
|---|---|
| `architect` | Independent design review of a plan before code, posted on the issue |
| `reviewer` | Independent code review with the design pass, posted on the PR |
| `tester` | Fill test gaps in existing code, failure paths first |

### `meta` — keep the workflow improving

| Skill | When to use |
|---|---|
| `create-skill` | Create or update a skill; fresh-agent dry run on two stacks before registering (a project's own skills, or this marketplace's) |
| `decision` | Record an architecture decision (ADR) with options, consequences and a revisit signal |
| `capture-lesson` | Turn a lesson from real work into a test, lint, gate or rule — and log it |

### `guardrails` — opt-in hooks

| Hook | What it does |
|---|---|
| Secret scan | Blocks `git commit` when staged, unstaged or untracked changes add something that looks like a key or token |
| No commits on main | Blocks `git commit` on `main`/`master` (set `GUARDRAILS_ALLOW_MAIN_COMMIT=1` to allow once) |

## Staying up to date

Lessons from real projects become skill changes through a written process: [docs/lessons.md](docs/lessons.md). Every plugin has a semantic version; changes are in [CHANGELOG.md](CHANGELOG.md). To contribute, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository layout

```
.claude-plugin/marketplace.json     the marketplace (lists every plugin)
plugins/<plugin>/.claude-plugin/plugin.json
plugins/<plugin>/skills/<skill>/SKILL.md (+ references/)
plugins/agents/agents/*.md
plugins/guardrails/hooks/hooks.json + scripts/
docs/                               workflow map, skill format, lessons, other agents
scripts/check.py                    CI checks (frontmatter, manifests, links, framework names, privacy)
scripts/install-skills.sh           install skills into another agent's folder
AGENTS.md                           rules for agents working on this repository
```

## License

MIT — see [LICENSE](LICENSE).
