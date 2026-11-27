#!/usr/bin/env bash
set -eu
command -v python3 >/dev/null 2>&1 || { echo 'Blocked: python3 is required for this guard.' >&2; exit 2; }
exec python3 "$(dirname "$0")/guard.py" secrets "$@"
