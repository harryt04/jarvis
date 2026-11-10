#!/usr/bin/env bash
# List copyable Jarvis skills and sibling Git repositories, numbered.
# Usage: discover.sh [jarvis_root]   (defaults to the repo containing this script)
set -euo pipefail
root="${1:-$(cd "$(dirname "$0")/../../.." && pwd)}"
# Siblings are relative to the primary checkout, so a linked worktree
# (e.g. a Treehouse slot) still finds the real ../ repos.
common="$(git -C "$root" rev-parse --path-format=absolute --git-common-dir)"
primary="$(dirname "$common")"
parent="${SKILL_COPY_PARENT:-$(cd "$primary/.." && pwd)}"
self="$(basename "$primary")"

echo "## Skills (source: $root/skills)"
i=0
for d in "$root"/skills/*/; do
  name="$(basename "$d")"
  [[ -f "$d/SKILL.md" && "$name" != "skill-copy" ]] || continue
  i=$((i+1))
  desc="$(awk '/^description:/{sub(/^description:[ ]*/,""); print; exit}' "$d/SKILL.md" | cut -c1-90)"
  printf 'S%d  %s — %s\n' "$i" "$name" "$desc"
done
[[ $i -gt 0 ]] || echo "(none found)"

echo
echo "## Sibling repos (in $parent)"
j=0
for d in "$parent"/*/; do
  name="$(basename "$d")"
  [[ "$name" != "$self" && -e "$d/.git" ]] || continue
  j=$((j+1))
  has=""
  [[ -d "$d/.claude/skills" ]] && has+=" claude"
  [[ -d "$d/.agents/skills" ]] && has+=" codex"
  printf 'R%d  %s%s\n' "$j" "$name" "${has:+  [existing:$has]}"
done
[[ $j -gt 0 ]] || echo "(none found)"
