#!/usr/bin/env bash
# Advisory guard runner: run-guard.sh <secrets|branch> [--git-hook]
# As a host PreToolUse hook it reads the hook JSON on stdin. Uses Bash builtins only,
# so a command without both "git" and "commit" is allowed even when python3 is missing.
set -u
check=$1
shift
dir=${BASH_SOURCE[0]%/*}
[ "$dir" = "${BASH_SOURCE[0]}" ] && dir=.
if [ "${1:-}" = "--git-hook" ]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "guardrails: python3 not found; $check check skipped (advisory hook)." >&2
    exit 0
  fi
  exec python3 "$dir/guard.py" "$check" --git-hook
fi
IFS= read -r -d '' input || true
case $input in *git*) ;; *) exit 0 ;; esac
case $input in *commit*) ;; *) exit 0 ;; esac
if ! command -v python3 >/dev/null 2>&1; then
  echo "guardrails: python3 not found; $check check skipped for this git commit (advisory hook)." >&2
  exit 0
fi
printf '%s' "$input" | python3 "$dir/guard.py" "$check"
