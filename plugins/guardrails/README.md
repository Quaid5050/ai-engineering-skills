# guardrails 2.0.0

Advisory command preflight and actual-index Git hooks with redacted results; host permissions and protected checks remain the enforcement boundary.

## What the hooks do
Both run as `PreToolUse` hooks on `Bash` (stdin JSON with `tool_input.command` and `cwd`; exit 2 with a message on stderr blocks).

| Hook | Blocks |
|---|---|
| `check-staged-secrets.sh` | A commit whose **added lines** match a credential pattern. The message names the file and line (`path:line`) and never prints the value; a file name that itself looks like a secret is withheld. |
| `no-commit-on-main.sh` | A commit on the default branch: `main`, `master` or the branch `origin/HEAD` points to. Detached HEAD is allowed. `GUARDRAILS_ALLOW_MAIN_COMMIT=1 git commit …` allows a deliberate bootstrap commit. |

## When they act
- A cheap Bash pre-filter exits at once unless the command contains both `git` and `commit`, so other commands cost nothing and work without Python.
- The command is then parsed like a shell would: only a segment that runs `git` with the `commit` subcommand counts, after optional `cd <dir> &&`, `VAR=value`, and the global options `-C <dir>` and `-c <key=value>`. Text in quoted arguments, heredoc bodies, `$(cat <<'EOF' … EOF)` messages and other commands' arguments (`grep commit`, `gh pr create --body "commit"`) never triggers it.
- What is scanned: the staged diff (`git diff --cached -U0`, one Git call); plus tracked working-tree changes for `git commit -a`/`-am`, the named paths for `git commit -- <paths>`, and what an earlier `git add` in the same command will stage (including untracked files). Binary files are skipped, as Git's diff skips them.
- **Fail closed on bypasses:** a commit that cannot be analysed is blocked with a reason: `eval`, `bash -c`/`sh -c`, a shell fed a heredoc, `sudo`/`xargs`/`env` wrappers, a variable-expanded command, subcommand or `-C` path, a commit inside `$(…)` or backticks, `--git-dir`/`--work-tree`, `GIT_*` or `PATH` changes, and `cd` to a non-literal path. Run a plain `git commit` instead.
- **Advisory, fails open on missing tools:** without `python3` the hook warns on stderr and allows the commit. Git aliases (`git ci`) and other ways of creating commits are not seen.

## As Git hooks
`python3 scripts/guard.py secrets --git-hook` and `python3 scripts/guard.py branch --git-hook` check the real index from a `pre-commit` hook.

Requires Python 3.8+ for the checks; the wrappers need Bash. See [host adapters](../../docs/other-agents.md) and [evaluation](../../docs/evaluation.md).
