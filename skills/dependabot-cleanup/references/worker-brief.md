# Dependabot cleanup worker brief

You own the assigned Dependabot PRs of one or more repositories. The goal is
to merge every one of them, each fixed against the freshly merged default
branch, or report why one can't be merged. The coordinator supplies the
repositories in order, with each one's checkout path, PR list, and diagnosis,
plus the authority and GitHub account rules.

Work through the repositories one at a time, in the given order, and finish
one repository's merges before you merge in the next. Only two repositories
may be merging at once across the whole run, and the coordinator plans for
your session to be one of them. You may use native subagents to prepare the
next repository in parallel: read its instructions, take its lease, run its
baseline checks, and draft its baseline fix. Don't launch T3 sessions.

Run every GitHub write as `GH_TOKEN=$(gh auth token -u harryt04) gh ...`. The
active `gh` account may not be able to merge. Never run `gh auth switch`.
Always pass `-R <owner/repo>` to `gh`. Without it, `gh` acts on the repository
of the current directory, which may be Jarvis.

## Set up once

1. Verify the checkout's `origin` matches the assigned repository. Read its
   agent instructions (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING`) and its CI
   workflow files, so you know the real checks and package manager.
2. Fetch, then take one Treehouse lease for the whole assignment:
   `treehouse get --lease --json --base <default-branch>` from the checkout.
   Use the returned path for everything. Verify that `HEAD` equals
   `origin/<default-branch>`. Never edit the primary checkout.
3. Install dependencies with the repository's own package manager and run its
   checks on the default branch. That is your baseline. Run the commands the CI
   workflow runs, not a guessed `typecheck` or `ci` script. Some builds need
   CI-only secrets or environment variables (`MONGO_CONNECTION_STRING`, for
   example), and the local Node version can differ from CI's. When a local
   step can't run for such a reason, say so, and let CI on the pushed head be
   the gate for that step. Public or build-time values that CI sets to dummies
   (`NEXT_PUBLIC_POSTHOG_KEY`, test-only auth secrets in the workflow's `env`)
   can take the same dummy values locally. A build that fails only because
   such a value is missing isn't a broken baseline. Never use real secrets.
   Pass `env` values from the workflow to the command, for example
   `env $(grep -E '^ +[A-Z_]+: ' .github/workflows/ci.yml | sed -E 's/^ +([A-Z_]+): *(.*)$/\1=\2/' | tr -d "'\"" | xargs) pnpm run ci`.

## Fix a shared cause first

If the baseline fails, or most assigned PRs fail the same check, fix that once
on the default branch rather than in every PR. Examples: add Dependabot's
lockfile to `.prettierignore`, or repair a test that broke on its own.

Make the fix on a branch `fix/dependabot-cleanup-baseline-<YYYY-MM-DD>` in
your worktree, and give the PR exactly the title
`fix(ci): repair checks for dependabot cleanup`. Every worker uses this title
and branch pattern, so the run's PRs look the same. Don't retitle Dependabot
PRs. Explain each root cause in the description, wait for CI, and merge it.

If branch protection requires a check that no job reports (the coordinator's
diagnosis says which), add a gate job with exactly that name. It `needs`
every real job, runs with `if: always()`, and fails unless every needed job
succeeded. That restores the required check without a settings change. Keep the fix minimal. Don't weaken or
delete checks to make them pass. If the only route to green is weakening a
check, stop and report it instead.

## Then, for each PR, oldest first

1. **Refresh the PR's state** (`gh pr view <n> --json mergeable,mergeStateStatus,statusCheckRollup,headRefOid`).
   If it's already merged or closed, record that and move on.
2. **Check out Dependabot's branch in your worktree:**
   `git fetch origin <head> <default>` then
   `git switch -C <head> origin/<head>`.
3. **Bring in the default branch** when it has moved, or when the PR conflicts
   or fails: `git merge origin/<default>`. Resolve conflicts by intent:
   - Lockfile conflicts: never hand-merge them. Take the default branch's
     lockfile (`git checkout origin/<default> -- <lockfile>`), keep the merged
     manifest, then re-apply the bump with the repository's package manager:
     `pnpm update <pkg>@<new-version>`, `npm install <pkg>@<new-version>`
     (or `npm update <pkg>` for an indirect dependency), `yarn up`, `uv lock
     --upgrade-package <pkg>`, and so on. A plain `--lockfile-only` regenerate
     isn't enough. Many Dependabot PRs bump indirect dependencies for security
     fixes, and a regenerate quietly keeps the old version. Confirm the new
     version made it in (`pnpm why <pkg>`, `npm ls <pkg>`) before you push.
   - pnpm indirect dependencies: `pnpm update <pkg>@<version>` writes an
     `overrides` entry into `package.json` when `<pkg>` isn't a direct
     dependency. Use `pnpm update --depth Infinity <pkg>` without a version
     instead. That form takes the newest version the parents allow, which can
     be newer than Dependabot's target. On 2026-11-10, a PR for
     `@hono/node-server` 1.19.18 resolved to 2.1.6. Compare `pnpm why` with
     the PR title, and report any difference. For pnpm repos,
     [scripts/refresh-pnpm-pr.sh](../scripts/refresh-pnpm-pr.sh) does the
     merge, lockfile reset, update, frozen install, and push in one step. It
     stops on any conflict outside `pnpm-lock.yaml`.
     If the PR's base is so stale that its lockfile type no longer exists on
     the default branch (an old npm PR after a pnpm migration, say), delete
     the stale lockfile, apply the manifest change, and generate the current
     lockfile type.
   - Manifest or workflow conflicts: keep Dependabot's new version for the bumped
     package and the default branch's state for everything else.
4. **Make it pass.** Run the repository's checks locally. If the bump itself
   breaks something, such as a major-version API change, fix the code on this
   branch. A new framework version can also expose old errors. For example,
   the Next.js 16.4 build type-checks every file `tsconfig.json` includes,
   test files too. It surfaced old type errors in test files, which needed
   test-only fixes. Keep the fix to what the upgrade requires. If it would take a large
   migration or product decisions, stop on this PR and report what it needs.
5. **Push normally:** `git push origin HEAD:<head>`. Never force-push. A push from
   Harry's account also re-runs CI with normal Actions secrets, which fixes
   failures caused only by Dependabot's restricted secrets. Dependabot stops
   rebasing a PR once someone else pushes to it. That's fine, because you merge
   it next.
6. **Wait for CI** on the new head. In a T3 session, call
   `watch_pull_request` for the PR and end your turn. T3 wakes you when the
   checks finish. Unwatch it after it merges. Outside T3, use
   `gh pr checks <n> --watch` where the host permits it. For a repository with
   no CI, your local checks on the exact pushed head are the gate. If your host
   forbids every form of waiting, stop and return the pushed PR numbers and
   head SHAs. Don't report them as merged.
7. **Merge** with an allowed method, pinned to the head you validated:
   `GH_TOKEN=$(gh auth token -u harryt04) gh pr merge <n> --squash --match-head-commit <sha>`.
   Use `--merge` or `--rebase` only when squash is disabled. If the merge is
   refused, re-read the state and repeat from step 1 rather than overriding. A
   refusal that says `refusing to allow an OAuth App to create or update
   workflow` means the PR edits `.github/workflows` and is behind the default
   branch: the `harryt04` token has no `workflow` scope. Merge the default
   branch into the PR and push over SSH, wait for CI, then merge. A
   refusal that says "base branch policy prohibits the merge" while every job
   is green usually means a required check never reports. Fix that with the
   baseline gate job, not with `--admin`. In a script, chain the next PR's
   refresh with `&&` after the merge, never with `;`. Otherwise a refused
   merge still pushes the next PR against the old base.

After each merge, the remaining PRs may conflict or need a refreshed lockfile.
Expect that, and always handle the next PR against the new default branch.

Dependabot can still rebase a PR after your push if it queued the rebase
earlier. That force-push replaces your commit with a head that is behind the
default branch. Green checks on a head you didn't push aren't your gate.
`--match-head-commit` with your own validated SHA refuses that merge. Refresh
the PR again and push.

Some failures only clear with time, like pnpm's `minimumReleaseAge` rejecting
a package published within the last day. Don't relax the policy. First,
refresh the PR anyway. Dependabot resolved the lockfile with the newest
transitive version. A local `pnpm update` respects the age policy and often
picks an older allowed version. On 2026-11-10, three better-auth PRs were
blocked on `jose@6.2.17`, and a refresh resolved `jose@6.2.16` or `6.2.3`.
All three merged hours before the gate. Only when the refresh still fails,
report the PR as `time-gated` with the time it should pass (publish time plus
the configured age), and move on to the next PR.

When a later PR becomes redundant, because an earlier merge already pulled in
the same or a newer version, leave it open and report it as `superseded`.
Dependabot closes those itself on its next run.

## Return

Return this per repository. For each assigned PR: number, outcome (`merged`, `fixed+merged`, `left open`,
`superseded`, `time-gated`), the merged commit or the reason it's still open, and what you
changed beyond the lockfile. Also return baseline-repair PR URLs, the checks
you ran, the worktree path, and anything the coordinator should tell other
workers, such as a cause shared across repos. Leave the lease in place. Cleanup
isn't part of this job.
