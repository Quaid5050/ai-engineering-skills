#!/usr/bin/env bash
# Copy (or link) every skill of this marketplace into one flat skills folder, for agents that read
# Agent Skills (SKILL.md) from a directory instead of installing Claude Code plugins.
#
#   scripts/install-skills.sh <target-skills-dir> [--link] [--plugins lifecycle,quality,...]
#
# Examples (check your tool's docs for its current path):
#   scripts/install-skills.sh ~/my-app/.agents/skills          # shared location many agents read
#   scripts/install-skills.sh ~/.codex/skills --link            # personal, kept in sync with this clone
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
target="${1:?usage: install-skills.sh <target-skills-dir> [--link] [--plugins a,b]}"; shift
mode=copy; only=""
while [ $# -gt 0 ]; do
  case "$1" in
    --link) mode=link ;;
    --plugins) only="$2"; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
  shift
done
mkdir -p "$target"
count=0
for skill in "$here"/plugins/*/skills/*/; do
  plugin="$(basename "$(dirname "$(dirname "$skill")")")"
  if [ -n "$only" ] && [[ ",$only," != *",$plugin,"* ]]; then continue; fi
  name="$(basename "$skill")"
  dest="$target/$name"
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then echo "skip $name: $dest exists (not ours)"; continue; fi
  rm -f "$dest"
  if [ "$mode" = link ]; then ln -s "${skill%/}" "$dest"; else cp -R "${skill%/}" "$dest"; fi
  count=$((count + 1))
done
echo "$mode: $count skills into $target"
echo "Agents (architect, reviewer, tester) are in plugins/agents/agents/*.md — see docs/other-agents.md."
