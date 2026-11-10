#!/usr/bin/env bash
# Upsert one Jarvis skill into one sibling repo for Claude and Codex.
# Usage: copy.sh <jarvis_root> <skill_name> <target_repo_path> [--dry-run]
# Adds or overwrites files; never deletes extra files already in the target.
set -euo pipefail
root="$1"; skill="$2"; target="$3"; dry="${4:-}"
src="$root/skills/$skill"
[[ -f "$src/SKILL.md" ]] || { echo "error: no skill at $src" >&2; exit 1; }
src="$(cd -P "$src" && pwd)"  # skills may be symlinks; copy their real contents
[[ -e "$target/.git" ]] || { echo "error: $target is not a git repo" >&2; exit 1; }

for dest_root in .claude/skills .agents/skills; do
  dest="$target/$dest_root/$skill"
  # Report what will change, file by file.
  while IFS= read -r -d '' f; do
    rel="${f#"$src"/}"
    if [[ ! -e "$dest/$rel" ]]; then echo "  add     $dest_root/$skill/$rel"
    elif ! cmp -s "$f" "$dest/$rel"; then echo "  update  $dest_root/$skill/$rel"
    fi
  done < <(find -L "$src" -type f -print0)
  if [[ -d "$dest" ]]; then
    while IFS= read -r -d '' f; do
      rel="${f#"$dest"/}"
      [[ -e "$src/$rel" ]] || echo "  kept    $dest_root/$skill/$rel (not in source)"
    done < <(find "$dest" -type f -print0)
  fi
  if [[ "$dry" != "--dry-run" ]]; then
    mkdir -p "$dest"
    cp -RL "$src"/. "$dest"/
  fi
done
