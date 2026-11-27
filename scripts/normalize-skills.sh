#!/usr/bin/env bash
# Keep the Jarvis skill layout in its one supported shape:
#   skills/<name>/            real directory, the only copy of each skill
#   .agents/skills/<name>     symlink -> ../../skills/<name>  (Codex, Antigravity)
#   .claude/skills            symlink -> ../skills            (Claude Code)
#
# `npx skills add|update` installs into .agents/skills/<name> as a real
# directory and links skills/<name> back to it. Run this afterwards to move the
# installed copy into skills/ and restore the links.
#
# Usage: scripts/normalize-skills.sh [--check]
#   --check  report anything out of shape and exit 1, changing nothing.
set -euo pipefail

root="$(cd -P "$(dirname "$0")/.." && pwd)"
cd "$root"
check=0
[[ "${1:-}" == "--check" ]] && check=1

problems=0
note() { problems=$((problems + 1)); printf '%s\n' "$*"; }
run() { [[ $check -eq 1 ]] || "$@"; }

mkdir -p skills .agents/skills

# Claude Code reads the whole skills/ directory through one link.
if [[ "$(readlink .claude/skills 2>/dev/null)" != "../skills" ]]; then
  note ".claude/skills is not a symlink to ../skills"
  if [[ $check -eq 0 ]]; then
    [[ -e .claude/skills && ! -L .claude/skills ]] && { echo "refusing to replace real directory .claude/skills" >&2; exit 1; }
    mkdir -p .claude && ln -sfn ../skills .claude/skills
  fi
fi

# A real directory in .agents/skills is an install that belongs in skills/.
for d in .agents/skills/*; do
  [[ -e "$d" || -L "$d" ]] || continue
  name="$(basename "$d")"
  [[ -d "$d" && ! -L "$d" ]] || continue
  note "move .agents/skills/$name -> skills/$name"
  if [[ -e "skills/$name" && ! -L "skills/$name" ]]; then
    echo "conflict: skills/$name and .agents/skills/$name are both real directories; reconcile by hand" >&2
    exit 1
  fi
  run rm -f "skills/$name"
  run mv "$d" "skills/$name"
done

# skills/ holds real directories only.
for s in skills/*; do
  [[ -L "$s" ]] || continue
  note "remove symlink $s (skills/ must hold real directories)"
  run rm "$s"
done

# Every skill gets exactly one relative link in .agents/skills.
for s in skills/*/; do
  name="$(basename "$s")"
  [[ -f "skills/$name/SKILL.md" ]] || { note "skills/$name has no SKILL.md"; continue; }
  if [[ "$(readlink ".agents/skills/$name" 2>/dev/null)" != "../../skills/$name" ]]; then
    note "link .agents/skills/$name -> ../../skills/$name"
    run ln -sfn "../../skills/$name" ".agents/skills/$name"
  fi
done

# Links whose skill no longer exists, or that point anywhere else.
for l in .agents/skills/*; do
  [[ -L "$l" ]] || continue
  name="$(basename "$l")"
  if [[ "$(readlink "$l")" != "../../skills/$name" || ! -f "skills/$name/SKILL.md" ]]; then
    note "remove stale link $l"
    run rm "$l"
  fi
done

if [[ $problems -eq 0 ]]; then
  echo "skills layout ok ($(find skills -mindepth 1 -maxdepth 1 -type d | wc -l) skills)"
elif [[ $check -eq 1 ]]; then
  echo "skills layout: $problems problem(s); run scripts/normalize-skills.sh to fix" >&2
  exit 1
else
  echo "skills layout fixed ($problems change(s))"
fi
