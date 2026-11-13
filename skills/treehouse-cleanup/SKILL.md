---
name: treehouse-cleanup
description: Reclaim Treehouse worktree slots whose branch's PR has already merged, stopping leftover node/dev-server processes in those slots, while leaving every in-progress slot and its processes alone. Use automatically, without being asked, whenever Treehouse pools are full or `treehouse get` would add yet another slot because every existing one is leased, and also for /treehouse-cleanup, "clean up my treehouses", "free up worktrees", "release stale leases", or "kill the node processes from merged branches". Not for removing unmerged work, destroying pools, or ordinary PR delivery.
---

# Treehouse cleanup

Sessions often end, or get killed, after their PR merges but before the agent
runs `treehouse return`. The lease stays, so the slot is never reused, and a
`next dev`/`vite`/Playwright process can keep running inside it. Treehouse's
own `prune` and `destroy --all` never touch a leased slot, and they judge
"merged" by ancestry, which misses squash merges. This skill closes that gap.
It only reclaims a slot when GitHub proves its work landed.

## Authority

Recorded in [working agreements](../../context/working-agreements.md#confirmed-treehouse-cleanup-authority-2026-11-10).
Any agent may run the reclaim when pools are full or Harry asks. The scope
covers slots whose verdict is `reclaim` from the script below, plus the
processes whose working directory is inside those slots. Everything else is
out of scope: unmerged, open-PR, closed-unmerged, dirty, or unverifiable slots,
any process outside a reclaimable slot, `destroy`, `--force`, and machine-wide
`killall`.

## 1. Survey (dry run)

Run the script from any directory. It reads every pool under
`$TREEHOUSE_ROOT` (default `~/.treehouse`):

```sh
python3 skills/treehouse-cleanup/scripts/cleanup.py            # all pools
python3 skills/treehouse-cleanup/scripts/cleanup.py --pool jarvis-8f4df2
```

From another repository's session, use the Jarvis checkout's absolute path to
the script. Each held slot gets a verdict:

- `reclaim`: the tree is clean, a PR for the branch is `MERGED`, no PR for it
  is still open, and local `HEAD` is the PR's head or an ancestor of it.
  Nothing in the slot would be lost.
- `keep`: an open PR, no merged PR (including closed-unmerged), uncommitted or
  untracked files, local commits after the merged head, or a detached HEAD.
  Those are possibly someone's live or abandoned-but-unsaved work. Leave
  them, and their processes, alone.
- `unknown`: `gh` failed (auth, network, rate limit). Treat it as `keep` and
  report it.

Processes are matched by working directory under the slot path, not by name.
That way a `node` belonging to an in-progress slot is never a candidate. The
script also excludes its own process ancestry. It reads `/proc` on Linux and
`lsof` on macOS.

Read the process list of each `reclaim` slot before you apply. A dev server,
test runner, or stray `git` is in scope. An interactive terminal is not: a
login shell (`-zsh`), a TUI such as `herdr`, or a `claude` session that Harry
left open there. Keep that slot with `--skip <pool>/<name>` and report it.

GitHub lookups use the active `gh` account. When a private repo does not
resolve, the script retries with the token of a logged-in account named like
the repo owner (`gh auth token --user <owner>`).

## 2. Reclaim

```sh
python3 skills/treehouse-cleanup/scripts/cleanup.py --apply
python3 skills/treehouse-cleanup/scripts/cleanup.py --apply --skip dexter-d89663/10
```

For each `reclaim` slot, the script sends SIGTERM to its processes, waits
`--grace` seconds (default 5), sends SIGKILL to any that remain, then runs
`treehouse return <path> --if-lease-id <id>`. The lease pin means a slot
re-leased since the survey is skipped, not stolen. It never passes `--force`.
A clean slot needs no reset prompt, so a prompt or failure is a signal to stop
and report, not to override.

If your own session's working directory is inside a reclaimable slot, `cd` out
first. Never reclaim the slot your current task is using, even when its PR has
merged and you are mid-follow-up.

## 3. Continue and report

After reclaiming, retry the `treehouse get` that prompted the cleanup. Report
briefly:

- slots returned (pool/name, branch, PR link)
- processes stopped, with names and PIDs
- slots kept, grouped by reason, so Harry can see abandoned work
  (closed-unmerged, dirty) that needs a human decision
- any `unknown` or failed returns

If nothing is reclaimable and the pool is still full, say so and continue with
a fresh slot, which Treehouse adds automatically. Don't widen the cleanup to
make room.
