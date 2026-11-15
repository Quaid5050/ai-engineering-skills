#!/usr/bin/env bash
# PreToolUse (Bash): before a `git commit`, block it when the changes about to be committed add something that looks
# like a secret (private keys, cloud/API keys, service-account JSON, tokens). Scans the staged diff and — because
# `git add . && git commit` and `git commit -a` stage inside the same command — unstaged changes to tracked files and
# new untracked files too. Prints file names only, never the matched value.
# A false positive is fixed by moving the value to configuration (example config files hold placeholders only).
cmd="$("$(dirname "$0")/read-command.sh")"
case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac

pattern='-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|"private_key"[[:space:]]*:|xox[baprs]-[0-9A-Za-z-]{10,}|gh[pousr]_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{40,}|sk_live_[0-9A-Za-z]{20,}|sk-[A-Za-z0-9_-]{32,}'

files_in_diff() { # prints files whose added lines match
  local file="" line
  git -c core.quotePath=false diff "$@" -U0 2>/dev/null | grep -E '^\+' | grep -qE -- "$pattern" || return 0
  while IFS= read -r line; do
    case "$line" in
      "+++ b/"*) file="${line#+++ b/}" ;;
      "+++ "*) file="" ;;
      "+"*) [ -n "$file" ] && printf '%s\n' "$line" | grep -qE -- "$pattern" && printf '%s\n' "$file" ;;
    esac
  done < <(git -c core.quotePath=false diff "$@" -U0 2>/dev/null)
  return 0
}

hits="$( { files_in_diff --cached; files_in_diff; \
  git ls-files --others --exclude-standard -z 2>/dev/null | xargs -0 grep -lE -- "$pattern" 2>/dev/null; } | sort -u | head -10)"
if [ -n "$hits" ]; then
  echo "Blocked: these files look like they add a secret (key, token or service-account JSON). Move the value to configuration or the environment and commit placeholders only:" >&2
  printf '%s\n' "$hits" | sed 's/^/  /' >&2
  echo "If the file is not meant to be committed, add it to .gitignore." >&2
  exit 2
fi
exit 0
