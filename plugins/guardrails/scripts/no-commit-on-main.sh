#!/usr/bin/env bash
# PreToolUse (Bash): block `git commit` while the current branch is the default branch (main or master).
# Work happens on a branch and lands through a pull request.
# Allow it (e.g. the first commit of a brand-new repository) either way:
#   - prefix the command:  GUARDRAILS_ALLOW_MAIN_COMMIT=1 git commit -m "chore: initial commit"
#   - or start the agent with GUARDRAILS_ALLOW_MAIN_COMMIT=1 in its environment.
[ "${GUARDRAILS_ALLOW_MAIN_COMMIT:-}" = "1" ] && exit 0
cmd="$("$(dirname "$0")/read-command.sh")"
case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac
# An explicit allow prefix in the command itself (the hook runs before the command, so an env prefix never reaches it).
if printf '%s' "$cmd" | grep -qE '(^|[;&|[:space:]])(export[[:space:]]+)?GUARDRAILS_ALLOW_MAIN_COMMIT=1([;&|[:space:]]|$)'; then
  exit 0
fi
dir="${CLAUDE_PROJECT_DIR:-.}"
branch="$(git -C "$dir" branch --show-current 2>/dev/null || git branch --show-current 2>/dev/null)"
case "$branch" in
  main|master)
    echo "Blocked: you are committing directly on '$branch'. Create a branch for the issue first (git switch -c <type>/<n>-<slug>)." >&2
    echo "To allow it once (e.g. the first commit of a new repository), prefix the command: GUARDRAILS_ALLOW_MAIN_COMMIT=1 git commit …" >&2
    exit 2 ;;
esac
exit 0
