# AI Engineering Skills

Risk-based engineering workflows for AI coding agents: **71 skills in 17 plugins**, shared foundations and optional platform references. Existing skill names and paths remain stable.

Load only what the task needs. Small reversible fixes use a short path; sensitive data, destructive migrations and uncertain external effects receive deeper review. Checklist duration is not evidence of quality.

## Start here

| Task | Route |
|---|---|
| Small, clear fix | `work-context` → scoped implementation → relevant verification |
| Ordinary feature | `new-feature` → short plan → `implement` → focused review |
| Sensitive or hard-to-reverse change | Independent pre-change review → failure tests → implementation → recovery evidence |
| Production incident | Authorized containment → investigation → recovery → postmortem |
| New platform | Shared engineering skill + the relevant reference |

See the [workflow](docs/engineering-workflow.md), [coverage tiers](docs/compatibility.md) and [evaluation evidence](docs/evaluation.md). Documented coverage is not certification of every platform.

## Install

### Claude Code

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install lifecycle@ai-engineering-skills
```

Add area plugins as needed. Manifests declare dependencies. Independent roles are in `agents`; opt-in command preflights are in `guardrails`. Verify your host's plugin, role and hook support.

### Other Agent Skills clients

Requires Python 3.10+; the installer uses the standard library.

```bash
git clone https://github.com/Quaid5050/ai-engineering-skills
cd ai-engineering-skills
python3 scripts/install_skills.py /path/to/project/.agents/skills --plugins lifecycle,backend --dry-run
python3 scripts/install_skills.py /path/to/project/.agents/skills --plugins lifecycle,backend
```

Required skills are included automatically. Copy mode is the default; `--link` is for trusted local development. See [host adapters and recovery](docs/other-agents.md).

## Catalogue

| Plugin | Capabilities |
|---|---|
| [agents](plugins/agents/README.md) | Independent reviewers and scoped tester |
| [ai](plugins/ai/README.md) | `agent-workflow`, `llm-integration`, `rag-pipeline` |
| [architecture](plugins/architecture/README.md) | `safe-refactoring`, `system-design` |
| [backend](plugins/backend/README.md) | `add-endpoint`, `add-file-upload`, `add-migration`, `add-scheduled-job`, `backend-conventions`, `data-check` |
| [data](plugins/data/README.md) | `data-pipeline`, `database-operations`, `ml-lifecycle` |
| [desktop](plugins/desktop/README.md) | `desktop-application` |
| [foundation](plugins/foundation/README.md) | `safe-agent-execution`, `work-context` |
| [guardrails](plugins/guardrails/README.md) | Advisory preflight and actual-index checks |
| [lifecycle](plugins/lifecycle/README.md) | `bootstrap-project`, `bugfix`, `ci`, `cleanup`, `create-pr`, `deploy-check`, `design-review`, `engineering-principles`, `feature-to-issues`, `file-bug`, `file-feature`, `implement`, `incident`, `investigate-bug`, `investigate-feature`, `merge`, `new-feature`, `observe`, `postmortem`, `pre-commit`, `release`, `shape-idea`, `spec`, `start-issue` |
| [meta](plugins/meta/README.md) | `capture-lesson`, `create-skill`, `decision` |
| [mobile](plugins/mobile/README.md) | `background-work`, `design-to-screen`, `device-test`, `home-widget`, `mobile-conventions`, `offline-queue`, `shared-core` |
| [operations](plugins/operations/README.md) | `infrastructure-change`, `recovery-drill`, `service-reliability` |
| [quality](plugins/quality/README.md) | `accessibility-audit`, `analytics-event`, `code-review`, `perf-check`, `security-privacy-review`, `static-catalogs`, `tdd`, `testing-doctrine`, `write-tests` |
| [security](plugins/security/README.md) | `identity-access`, `supply-chain`, `threat-model` |
| [specialist](plugins/specialist/README.md) | `specialized-engineering` |
| [systems](plugins/systems/README.md) | `concurrency-networking`, `memory-and-ffi` |
| [web](plugins/web/README.md) | `add-web-page`, `build-web-screen`, `web-conventions` |

The [machine-readable catalogue](catalog/skills.json) includes required dependencies, resources, owners and conservative support tiers. Regenerate with `python3 scripts/update_catalog.py`.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/check.py
python -m unittest discover -s tests -v
claude plugin validate . --strict
```

The real container boundary test is opt-in locally: `RUN_CONTAINER_TESTS=1 python -m unittest discover -s tests -p test_execution_boundary.py -v`. It requires Docker and its pinned image; never mount credentials or the Docker socket into agent execution environments.

## Audit and migration

The [historical audit](docs/audits/2026-11-26/comprehensive-audit.md) is pinned to the original revision. [Remediation](docs/remediation.md) records implementation and evidence limits; [migration notes](docs/migration-v2.md) explain breaking changes. Contributions: [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE).
