# Dependabot cleanup worker brief

You own one repository's assigned Dependabot PRs. The goal is to merge every
one of them, each fixed against the freshly merged default branch, or report
why one can't be merged. The coordinator supplies the repository, checkout
path, PR list, diagnosis, and authority. Don't spawn agents or watch PRs.

## Set up once

1. Verify the checkout's `origin` matches the assigned repository. Read its
   agent instructions (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING`) and its CI
   workflow files, so you know the real checks and package manager.
2. Fetch, then take one Treehouse lease for the whole assignment:
   `treehouse get --lease --json --base <default-branch>` from the checkout.
   Use the returned path for everything. Verify that `HEAD` equals
   `origin/<default-branch>`. Never edit the primary checkout.
3. Install dependencies with the repository's own package manager and run its
   checks on the default branch. That is your baseline.

## Fix a shared cause first

If the baseline fails, or most assigned PRs fail the same check, fix that once
on the default branch rather than in every PR. Examples: add Dependabot's
lockfile to `.prettierignore`, or repair a test that broke on its own.

Make the fix on a branch `fix/dependabot-cleanup-baseline-<date>` in your
worktree, and give the PR the title
`fix(ci): repair checks for dependabot cleanup`. Explain the root cause in the
description, wait for CI, and merge it. Keep the fix minimal. Don't weaken or
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
     If the PR's base is so stale that its lockfile type no longer exists on
     the default branch (an old npm PR after a pnpm migration, say), apply the
     manifest change and generate the current lockfile type.
   - Manifest or workflow conflicts: keep Dependabot's new version for the bumped
     package and the default branch's state for everything else.
4. **Make it pass.** Run the repository's checks locally. If the bump itself
   breaks something, such as a major-version API change, fix the code on this
   branch. Keep the fix to what the upgrade requires. If it would take a large
   migration or product decisions, stop on this PR and report what it needs.
5. **Push normally:** `git push origin HEAD:<head>`. Never force-push. A push from
   Harry's account also re-runs CI with normal Actions secrets, which fixes
   failures caused only by Dependabot's restricted secrets. Dependabot stops
   rebasing a PR once someone else pushes to it. That's fine, because you merge
   it next.
6. **Wait for CI** on the new head, using whatever waiting mechanism the host
   allows (`gh pr checks <n> --watch` where it's permitted). For a repository
   with no CI, your local checks on the exact pushed head are the gate.
7. **Merge** with an allowed method, pinned to the head you validated:
   `gh pr merge <n> --squash --match-head-commit <sha>`. Use `--merge` or
   `--rebase` only when squash is disabled. If the merge is refused, re-read
   the state and repeat from step 1 rather than overriding.

After each merge, the remaining PRs may conflict or need a refreshed lockfile.
Expect that, and always handle the next PR against the new default branch.

Some failures only clear with time, like pnpm's `minimumReleaseAge` rejecting
a package published within the last day. Don't relax the policy. Report the PR
as `time-gated` with the time it should pass (publish time plus the
configured age), and move on to the next PR.

When a later PR becomes redundant, because an earlier merge already pulled in
the same or a newer version, leave it open and report it as `superseded`.
Dependabot closes those itself on its next run.

## Return

For each assigned PR: number, outcome (`merged`, `fixed+merged`, `left open`,
`superseded`, `time-gated`), the merged commit or the reason it's still open, and what you
changed beyond the lockfile. Also return baseline-repair PR URLs, the checks
you ran, the worktree path, and anything the coordinator should tell other
workers, such as a cause shared across repos. Leave the lease in place. Cleanup
isn't part of this job.
