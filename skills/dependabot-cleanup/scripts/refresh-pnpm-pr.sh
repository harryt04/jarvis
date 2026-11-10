#!/usr/bin/env bash
# Refresh one pnpm Dependabot PR against the default branch and push it.
#
# usage: refresh-pnpm-pr.sh <worktree> <head-branch> <package> [version] [default-branch]
#
# Run it inside a Treehouse worktree of the target repository, only after the
# previous PR in that repository has merged. Give [version] only for a direct
# dependency. For an indirect one, `pnpm update <pkg>@<version>` writes an
# `overrides` entry, so the version-free `--depth Infinity` form is used. That
# form resolves to the newest version the parents allow, which can be newer
# than Dependabot's target, so compare the printed `pnpm why` line with the PR
# title and report any difference.
#
# The script stops (exit 2) on a conflict outside pnpm-lock.yaml. It does not
# run the repository's checks: run the commands from its CI workflow before
# relying on the push. CI on the pushed head is the merge gate.
set -euo pipefail
worktree=$1 head=$2 pkg=$3 version=${4:-} default=${5:-master}
cd "$worktree"
git merge --abort 2>/dev/null || true
git fetch -q origin "$head" "$default"
git switch -q -C "$head" "origin/$head"
git merge -q --no-edit "origin/$default" >/dev/null 2>&1 || true
conflicts=$(git diff --name-only --diff-filter=U)
if [ -n "$conflicts" ] && [ "$conflicts" != pnpm-lock.yaml ]; then
  echo "conflict outside pnpm-lock.yaml:" >&2
  echo "$conflicts" >&2
  exit 2
fi
git checkout "origin/$default" -- pnpm-lock.yaml
if [ -n "$version" ]; then
  pnpm update "$pkg@$version" >/dev/null
else
  pnpm update --depth Infinity "$pkg" >/dev/null
fi
pnpm install --frozen-lockfile >/dev/null
echo "resolved: $(pnpm why "$pkg" 2>/dev/null | grep -oE "^$pkg@[0-9][^ ]*" | sort -u | tr '\n' ' ')"
git add -A
git diff --cached --quiet || git commit -q -m "Merge $default and refresh lockfile for $pkg"
git push -q origin "HEAD:$head"
echo "pushed: $(git rev-parse HEAD)"
