# Agent rules for this repository

This repository is a skills and agents marketplace. You are editing **instructions other agents will follow on other people's projects**, so precision matters more than volume.

## Layout
- `.claude-plugin/marketplace.json` lists every plugin; `plugins/<plugin>/.claude-plugin/plugin.json` describes one.
- Skills: `plugins/<plugin>/skills/<skill>/SKILL.md`, stack detail in `references/<stack>.md` beside it.
- Agents: `plugins/agents/agents/*.md`. Hooks: `plugins/guardrails/hooks/hooks.json` + `scripts/`.
- The house structure every skill follows: [docs/skill-format.md](docs/skill-format.md). The lifecycle map: [docs/engineering-workflow.md](docs/engineering-workflow.md).

Install development dependencies with `python3 -m pip install -r requirements-dev.txt`.

## Commands
| Task | Command |
|---|---|
| All repository checks (CI runs the same) | `python3 scripts/check.py` |
| Regression tests | `python3 -m unittest discover -s tests -v` |
| Regenerate catalogue | `python3 scripts/update_catalog.py` |
| One check | `python3 scripts/check.py frameworks` (also: `manifests catalog skills agents links privacy`) |
| Validate the marketplace | `claude plugin validate . --strict` |
| Validate one plugin | `claude plugin validate plugins/<plugin> --strict` |
| Try a plugin locally without installing | `claude --plugin-dir plugins/<plugin>` |
| Install skills into another agent's folder | `scripts/install-skills.sh <dir> [--link] [--plugins a,b]` |

## Rules
1. **Framework-agnostic core.** No framework, language or vendor names in a `SKILL.md`; they go in `references/<stack>.md`. `scripts/framework-terms.txt` is the list CI enforces.
2. **Every skill reads the target project first** (`## 0. Read the project`) and lets the project win on facts.
3. **No private data.** No product or customer names, people's names, emails, phone numbers, issue numbers from other projects, internal paths or URLs, tokens or keys. Examples use toy domains (shop, bookings, notes).
4. **Never weaken a safety, privacy or testing rule** to make a skill shorter.
5. **Versioning.** A change to a plugin bumps its version in `plugin.json`, in its marketplace entry and in every skill's `metadata.version`, and adds a `CHANGELOG.md` entry (rules in [CONTRIBUTING.md](CONTRIBUTING.md)).
6. **Lessons** follow [docs/lessons.md](docs/lessons.md): a lesson becomes a check, a gate or a rule, and is logged.
7. A new or changed skill gets a fresh-agent dry run (`create-skill` §3) before it is merged.
8. Work on a branch, conventional commits, a PR with the checks green. CI runs on GitHub-hosted runners only; never attach a self-hosted runner to this public repository.
