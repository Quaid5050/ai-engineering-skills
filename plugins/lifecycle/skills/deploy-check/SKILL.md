---
name: deploy-check
description: "Pre-merge scan of a change for what breaks real users after it is deployed — non-additive API contract changes that installed clients still call, migrations that rewrite or lock big tables, native or bridge changes that need a store release, new permissions, background behaviour, push payloads, configuration and secrets per environment (including trusted-proxy settings and tokens in URLs), realtime method names, feature flags, rollback, and major dependency bumps — with a verdict, deploy order and rollback plan. Use before merging anything that touches an API, data, native code, config or infrastructure. Trigger on /deploy-check, 'is this safe to merge', 'breaking change check', 'will this break old app versions', 'pre-merge check', 'deploy order'."
argument-hint: "[PR or branch]"
license: MIT
metadata:
  version: "2.0.0"
---

# Deploy check

Scan `$ARGUMENTS` (a PR or branch; default the current branch) for anything that can break real users once merged and deployed. Clients make this hard: **old app versions stay installed for months** and keep calling the API; browsers keep old bundles open for hours.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

From `AGENTS.md` and the repo: where the API contract lives, the migration folder, native/bridge definitions, permission manifests, infrastructure and environment config, the release paths (`release`), the oldest client version still supported, and the environments that exist.

```bash
git diff --stat origin/main...HEAD
git diff origin/main...HEAD -- '<contract path>' '<migrations path>' '<bridge definitions>' '<permission manifests>' '<infra/config paths>' .github/
gh pr diff <PR> --name-only            # a PR without checking it out
```

Quote pathspecs with `**`: some shells expand unquoted globs and abort on no match.

## 1. Checks

| # | Area | Breaks when | Required |
|---|---|---|---|
| 1 | **API contract** | A path, field or enum value is removed or renamed; a field becomes required; a type or error code changes | Additive only while released clients use it. A removal keeps the old shape until the oldest supported client no longer calls it, or goes to a new path version. List every non-additive change in the contract diff. |
| 2 | **Migrations** | Table rewrite or long lock on a large table; NOT NULL without default; dropping a column running code still reads | Expand → migrate → contract across separate deploys; read the generated SQL (`add-migration`, backend plugin); engine/version-appropriate index creation; backfills as jobs, not inside the migration |
| 3 | **Native / bridge** | The client calls a native method the installed binary does not have | Mobile native code, bridge definitions, plugins and manifests require an appropriate binary/store release; desktop uses signed packages and a verified updater; the new code tolerates an older native side |
| 4 | **Permissions** | A new OS permission or usage description | Store release, review notes, the permission explanation screen updated, privacy policy and store data-safety forms updated |
| 5 | **Background behaviour (mobile)** | Sync intervals, background tasks, foreground services change | `device-test` (mobile plugin) done and battery recorded |
| 5b | **Server scheduling and workers** | A schedule or job changes; a rolling or blue/green deploy runs **two schedulers** at once; workers are killed mid-job | Coordination appropriate to the runner (leader, clustered scheduler or deduplicated triggers); jobs idempotent with a durable outbox with explicit completion state (`add-scheduled-job`, backend plugin); workers drained gracefully; a job's payload shape stays readable by the old and the new worker |
| 6 | **Push / message payloads** | Old clients cannot parse new payloads | Additive fields only; unknown types ignored without crashing |
| 7 | **Config & secrets** | A new setting is absent in an environment | Placeholder in the example env file; set in every environment **before** the deploy; the service fails fast at start-up if missing. **Reverse proxy:** the trusted-proxy setting must name the proxy in front of the service, or every caller shares the proxy's address — and its rate-limit budget; never trust a network clients can send from. |
| 8 | **Realtime** | A realtime socket method, channel or event is renamed; a token travels in a URL query string | Same rule as the API: additive, keep old names until old clients are gone. Tokens in query strings are stripped or redacted from every proxy, load balancer and access log before the first deploy. |
| 9 | **Feature flags** | Risky behaviour ships on for everyone | Safety-critical or privacy changes behind a flag or staged rollout when possible; each flag has a removal condition |
| 10 | **Rollback** | No way back | Say how: revert + redeploy, roll back the patch, halt the staged rollout. For migrations: is the down path tested, or is roll-forward the plan? |
| 11 | **Dependencies** | Major version bumps | Changelog read; every affected build done; native dependencies → store release |
| 12 | **Data exposure** | A new field, endpoint or log line carries personal data | `security-privacy-review` (quality plugin) |

**Gate:** every row is marked *n/a*, *safe*, or *needs action* with the action.

## 2. Output

```markdown
## Deploy check: <PR>
Release path: backend | web | mobile patch/store | signed desktop/package | model/data rollout (+ why)
Verdict: safe | safe with steps | not safe yet

| # | Area | Finding | Action before / after merge |
|---|---|---|---|

Deploy order: 1. … 2. …
Rollback: …
```

## Rules

- Post the output on the PR as one comment `## Deploy check — <short head SHA>`: it supplies the applicable deployment gate in `merge`.
- Anything unsafe in rows 1–3, 5b or 7 blocks the merge until fixed or the owner accepts the risk explicitly (quote them in the PR).
- Never change an environment, secret or deploy setting from this skill; list the action and who does it.
- When unsure which release path applies, it is the slower, safer one.

## Composition

| From | This skill | To |
|---|---|---|
| `create-pr`, `ci` | Verdict + deploy order | `merge`, then `release` |
| `add-endpoint`, `add-migration` (backend), `background-work` (mobile) | Their compatibility rules are checked here | — |
