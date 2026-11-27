#!/usr/bin/env bash
# Advisory: block a git commit on the default branch (detached HEAD is allowed).
d=${BASH_SOURCE[0]%/*}
[ "$d" = "${BASH_SOURCE[0]}" ] && d=.
exec "$BASH" "$d/run-guard.sh" branch "$@"
