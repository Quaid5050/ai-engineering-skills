# Using these skills with other agents

Every skill is a standard [Agent Skills](https://agentskills.io/specification) folder (`<name>/SKILL.md` plus optional `references/`), so any agent that reads Agent Skills can load them. Only the Claude Code plugin wrapper (`plugin.json`, the marketplace file, hooks and namespaced agents) is Claude Code-specific.

## 1. Install the skills

```bash
git clone https://github.com/Quaid5050/ai-engineering-skills
cd ai-engineering-skills
scripts/install-skills.sh <skills-folder> [--link] [--plugins lifecycle,quality,backend]
```

The script flattens `plugins/*/skills/*` into one folder. Typical folders (they change between versions — check your tool's docs):

| Agent | Project folder | Personal folder |
|---|---|---|
| Shared location read by many agents | `.agents/skills/` | `~/.agents/skills/` |
| Codex | `.agents/skills/` or `.codex/skills/` | `~/.codex/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

`--link` makes symlinks, so `git pull` in the clone updates every project. Copy instead when the project must not depend on your clone.

Skill references in the text name plugins ("`code-review` (quality plugin)"). After a flat install the plugin name does not matter: the skill is found by its name.

## 2. Point the agent at the workflow

Add to the project's `AGENTS.md` (most agents read it):

```markdown
## Workflow
This project uses the AI Engineering Skills workflow: docs/engineering-workflow.md in
https://github.com/Quaid5050/ai-engineering-skills. Before any step that has a skill
(new-feature, start-issue, design-review, implement, code-review, merge, …), load and follow it.
```

`bootstrap-project` writes a full `AGENTS.md` for a new repository.

## 3. The review agents without subagents

`architect`, `reviewer` and `tester` (`plugins/agents/agents/*.md`) are role descriptions. Their value is **independence**: they review work they did not write, with no access to the conversation that wrote it.

- **Agent supports subagents / custom agents:** copy the files into its agents folder (the frontmatter `name`, `description` and `tools` map to most tools' formats).
- **No subagents:** open a **new session** (fresh context), paste the agent file's body as the first instruction, and give it only the issue or PR link. Never run the review in the same session that wrote the code — and if you must, the posted review says it was not independent.

## 4. Lessons from your project

Installed or copied skills are a cache of this repository. When `capture-lesson` or `postmortem` finds a lesson, encode it in your project (`AGENTS.md`, conventions, tests, your own skills) and, if it is general, open an issue on this repository — do not edit the copied skill files, a later update overwrites them.

## 5. The hooks

The `guardrails` hooks are plain shell scripts (`plugins/guardrails/scripts/`). Outside Claude Code, use them as git hooks:

```bash
# .git/hooks/pre-commit — runs the secret scan on what is about to be committed
echo '{"tool_input":{"command":"git commit"}}' | bash /path/to/ai-engineering-skills/plugins/guardrails/scripts/check-staged-secrets.sh
```
