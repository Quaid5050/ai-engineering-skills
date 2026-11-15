#!/usr/bin/env bash
# Prints the Bash command from a PreToolUse hook payload on stdin. Empty when it cannot be read.
if command -v python3 >/dev/null 2>&1; then
  python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("tool_input",{}).get("command",""))
except Exception: print("")'
elif command -v jq >/dev/null 2>&1; then
  jq -r '.tool_input.command // ""' 2>/dev/null
else
  echo "guardrails: neither python3 nor jq found; hook skipped" >&2
fi
