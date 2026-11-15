# guardrails 1.0.0

Opt-in hooks: block a commit that adds something that looks like a secret, and block commits made directly on the main branch.

## Install

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install guardrails@ai-engineering-skills
```

## Hooks

- `PreToolUse` on Bash, `git commit`: `scripts/check-staged-secrets.sh` blocks a commit whose staged, unstaged or untracked changes add something that looks like a key or token (file names are printed, never the value).
- `PreToolUse` on Bash, `git commit`: `scripts/no-commit-on-main.sh` blocks commits on `main`/`master`; `GUARDRAILS_ALLOW_MAIN_COMMIT=1` allows one (e.g. the first commit of a new repository).
- Needs `bash` and `python3` or `jq`. Outside Claude Code, use the scripts as git hooks ([docs/other-agents.md](../../docs/other-agents.md)).

See the [catalogue](../../README.md#catalogue) and the [workflow map](../../docs/engineering-workflow.md). License: MIT.
