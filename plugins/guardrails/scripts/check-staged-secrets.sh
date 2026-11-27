#!/usr/bin/env bash
# Advisory: block a git commit whose added lines match a credential pattern.
d=${BASH_SOURCE[0]%/*}
[ "$d" = "${BASH_SOURCE[0]}" ] && d=.
exec "$BASH" "$d/run-guard.sh" secrets "$@"
