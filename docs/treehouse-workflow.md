# Portable session and Treehouse workflow

Confirmed policy: Harry's instruction, 2026-11-09; see the
[owning agreement](../context/working-agreements.md#confirmed-session-refresh-worktree-and-pr-policy-2026-11-09).
This is an agent procedure, not an installed startup hook or sync service.

## Session-start refresh

1. Locate the primary Jarvis checkout from the machine binding or known checkout,
   not by assuming a sibling of a task worktree. Verify its origin identifies
   `harryt04/jarvis`, then inspect `git status --short --branch`,
   `git worktree list`, and `git fetch origin`. Confirm `origin/main` exists.
2. In a clean primary checkout already on `main`, use
   `git merge --ff-only origin/main`. Never switch branches over existing work,
   reset, force-update, or automatically stash. A diverged main needs explicit
   reconciliation, not a destructive refresh.
3. If the checkout is dirty, diverged, or on an in-progress task branch, leave it
   intact. Read current memory directly with `git show origin/main:AGENTS.md`,
   `git show origin/main:README.md`, and the corresponding `context/` files;
   retrieve other referenced files from that same fetched revision as needed.
   Keep local task changes distinct from the latest merged memory.
4. Re-read the updated startup instructions, required context, and relevant
   project routing. A fetch alone does not reload a harness's prompt. Report a
   network/authentication failure and the available revision before relying on
   stale memory; do not claim freshness without a successful fetch.

Refresh Jarvis even for tasks in another repository. Pending PR memories are
not shared default-branch memory until merged. No cross-provider startup hook
or machine-wide bridge is installed by this documentation change.

## Install or locate Treehouse

Upstream: [kunchenguid/treehouse](https://github.com/kunchenguid/treehouse).
Check `command -v treehouse`, `treehouse --version`, and the installed command
help first. Also check `~/.local/bin/treehouse` when PATH is incomplete.

On macOS/Linux, download and inspect the upstream installer, then run it:

```sh
curl -fsSL https://kunchenguid.github.io/treehouse/install.sh -o /tmp/treehouse-install.sh
cat /tmp/treehouse-install.sh
mkdir -p "$HOME/.local/bin"
PATH="$HOME/.local/bin:$PATH" sh /tmp/treehouse-install.sh
export PATH="$HOME/.local/bin:$PATH"
treehouse --version
treehouse get --help
```

The reviewed installer prefers `~/.local/bin` when it is on PATH, otherwise
`/usr/local/bin` and possibly sudo. Prefer the user-writable location. Inspect
the current installer rather than assuming this behavior never changes. Keep
machine PATH setup local, outside Jarvis memory. Upstream also documents
Windows PowerShell installation (`irm https://kunchenguid.github.io/treehouse/install.ps1 | iex`),
Nix (`nix profile add github:kunchenguid/treehouse`), and Go
(`go install github.com/kunchenguid/treehouse/v3@latest`). Select the supported
method for the machine and verify its installed help. If installation fails,
report the concrete blocker; do not silently use a plain checkout instead.

## Acquire and verify a task worktree

Resolve project identity through the registry and brief, then verify the live
remote, instructions, Git state, and existing Treehouse leases. Read
`~/.agents/worktree-workflow.md` when available. Reuse the existing task lease
when resuming, preserving its branch and edits; do not reacquire or reset it.

For a new independent Jarvis task, fetch origin, then:

```sh
treehouse get --lease --json --base main -b docs/example-task
```

Use the returned absolute path for every subsequent edit/check/commit. Verify
`git rev-parse HEAD` matches `git rev-parse origin/main` in that worktree before
editing. Treehouse v3.1.8 expects `--base main`, not `--base origin/main`; local
and remote base selection can differ, so the equality check matters. If they
differ, preserve the allocated worktree and resolve the base before editing;
never assume the inferred base is fresh. For another repository, discover its
actual default branch instead of hardcoding `main`. Dependent tasks may require
an explicitly chosen local base; record that dependency and verify its SHA.

A durable `--lease` keeps the worktree reserved across noninteractive tool
calls. Do not use interactive subshell exit behavior as a substitute for a
lease. Keep dependency installs and build output in the task worktree, and
preserve concurrent work. This policy does not authorize spawning agents.

## Deliver

Run the target's applicable checks, review the diff for private data and scope,
commit the task changes, push the task branch normally, and create or update a
PR against the intended base. Return the PR link and validation result. Do not
merge, deploy, push directly to main, or clean up the worktree without the
applicable authority. Leave the lease available for review/resumption; record
its path in the task handoff rather than permanent portable memory. Commands
such as `treehouse return`, `destroy`, and `prune` may reset worktrees or stop
processes; they are cleanup, not a required PR delivery step.
When pools fill with slots whose PRs already merged, use the
[treehouse-cleanup skill](../skills/treehouse-cleanup/SKILL.md), which returns
only verified-merged, clean slots.

## Verification limits

Observed 2026-11-09: installed upstream Treehouse v3.1.8 on Linux arm64 in a
user bin directory; fetched and fast-forwarded a clean Jarvis main; acquired a
leased task branch with `--base main` and verified it against `origin/main`.
The remote-prefixed base was rejected by this version. Windows, macOS, Nix,
Go installation, dirty/diverged refresh cases, and automatic provider startup
loading were not exercised in this task. Recheck upstream guidance and CLI help
when versions change.
