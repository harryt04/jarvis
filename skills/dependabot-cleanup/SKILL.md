---
name: dependabot-cleanup
description: Merge every open Dependabot PR across Harry's harryt04/* GitHub repositories, fixing merge conflicts and failing CI in Treehouse worktrees first, and keep sweeping until no new Dependabot PRs appear during the session. Use for /dependabot-cleanup, "merge all my dependabot PRs", "clear out the dependency bumps", "dependabot is piling up", or a dry run of what such a sweep would do, even when the user doesn't say "skill". Not for application security reviews or advisory triage without merging (use security-review).
---

# Dependabot cleanup

The deliverable is that every Dependabot PR open when the skill starts, plus
every one that appears while it runs, ends up merged, or is reported with a
concrete reason it couldn't be. One coordinator (this session) scans, picks
the order, and dispatches one subagent worker per repository. Each worker
fixes and merges its repository's PRs in a Treehouse worktree, following
[the worker brief](references/worker-brief.md).

Workers merge in their own repository, not the coordinator. Merging one bump
usually conflicts the next one's lockfile, so each PR has to be fixed against
the freshly merged default branch right before it merges. Sending every PR
back to the coordinator would add a round trip to each step.

## Authority

Merge authority is confirmed in
[working agreements](../../context/working-agreements.md#confirmed-dependabot-cleanup-merge-authority-2026-11-10).
It covers Dependabot-authored PRs in live `harryt04/*` repositories, plus
baseline-repair PRs a worker opens in this run to make a default branch's
checks pass. Merge only with the repository's allowed methods. No admin
overrides, no bypassed protections, no force-pushes. Never close Dependabot
PRs, dismiss alerts, deploy by hand, change Coolify settings, or clean up
worktrees. Merges can trigger a repository's automatic deployments, so the
dispatch pacing below matters.

## Dry run

When Harry asks for a dry run, preview, or plan, or passes `--dry-run`, stop
after step 3. Report the scan, the per-repo diagnosis, and the order you would
dispatch in. Read-only investigation is fine (PR diffs, CI logs, default-branch
runs). Don't acquire worktrees, push, comment, or merge.

## 1. Refresh and scan

Follow the Jarvis `AGENTS.md` session-start refresh. Keep run state outside
Git under `~/.jarvis/dependabot-cleanup/<YYYY-MM-DD-HHMM>/`. Then scan:

```sh
python3 skills/dependabot-cleanup/scripts/scan.py --catalog projects/catalog.json \
  --seen ~/.jarvis/dependabot-cleanup/<run>/seen.json            # table for you
python3 skills/dependabot-cleanup/scripts/scan.py --catalog projects/catalog.json \
  --seen ~/.jarvis/dependabot-cleanup/<run>/seen.json --format json > .../scan-1.json
```

The scan reads the live repo list, not the catalog. It drops archived repos,
forks, and retired catalog ids, and lists them in the "Excluded" line. Pass
`--repos` or `--skip` when Harry narrows the scope. Save the first scan's PR
URLs as the run's starting set; the final report accounts for each of them.

States: `ready` (green, mergeable), `ready-no-ci` (no checks ran),
`ci-pending`, `ci-failing`, `conflicting`, `blocked`. `MAJOR` marks a
major-version bump. Majors follow the same rules as other bumps; passing
checks are the safety gate.

## 2. Diagnose each repository before dispatching

Spend a few read-only minutes per repository so each worker starts from the
real problem:

- When several PRs in one repo fail the same check, read one failing log
  (`gh run view <id> --log-failed`). They usually share a single cause, such
  as Prettier rejecting Dependabot's lockfile formatting, a broken default
  branch, or a missing secret. One baseline fix then clears every PR.
- Check the default branch's latest CI run on the same workflow. If it fails
  too, the PRs aren't to blame.
- Note which PRs touch the same lockfile. They will cascade into conflicts
  as their neighbors merge.

Record the diagnosis per repo in the run directory. It goes into the worker
prompt.

## 3. Plan the dispatch

Find each repo's local checkout. It is the scan's `local_folder` as a sibling
of the primary Jarvis checkout (for example `../scaffolding` for
`personal-project-scaffolding`). Verify its `origin`. If a repository has no
local checkout, clone it as a sibling only when Harry agrees; otherwise
report it as blocked.

Order repositories so the cheap ones go first: all-`ready` repos, then
conflicts, then CI failures. Every merge into a Coolify-hosted app queues a
deployment. The server builds two at a time and cancels superseded builds of
the same app
([burst record](../../docs/research/coolify-deployment-burst-2026-11-09.md)),
so run **at most two repository workers at once**. That keeps cross-repo
deploys within the build limit, while one repo's back-to-back merges just
supersede each other.

In a dry run, stop here and report (see step 6 for the format).

## 4. Dispatch workers

Spawn one subagent per repository, two at a time, with the native subagent
tool. Wait for each pair before starting the next, since the cap is the point.
Each prompt contains:

- the full text of [references/worker-brief.md](references/worker-brief.md)
- the verified repo identity, default branch, and local checkout path
- the PRs assigned to this worker (number, URL, head branch, state, failing
  checks), as JSON from the scan
- your step 2 diagnosis
- the authority section above, verbatim

Workers don't spawn more agents and don't watch PRs. Each returns a per-PR
outcome with a reason and URLs for any baseline-repair PRs. Follow the host's
PR-linking rules for PRs you or the workers create or push to.

If a worker reports a cause that applies to other repos (the same Prettier
lockfile problem in several Next.js repos, say), add it to the remaining
workers' diagnosis.

## 5. Rescan until quiet

After every batch, rescan with the same `--seen` file. PRs marked `NEW`
appeared during the session: Dependabot often opens follow-ups or recreated
PRs after merges. Dispatch workers for repos with new or still-actionable PRs.
Then rescan again.

Workers report `time-gated` PRs with the time they should pass. If that time
falls within the session, re-dispatch the repo's worker after it. Otherwise
report the gate time so Harry can rerun the skill later.

Stop when a full scan has no `NEW` PRs and every remaining PR has a reported
reason, or after a third pass that makes no progress. Before stopping, wait
about two minutes and scan once more. Dependabot reacts to merges
asynchronously, and this final scan catches the PRs it opens late.

## 6. Report

Return:

- one table: repo, PR, title, outcome (`merged`, `fixed+merged`,
  `time-gated`, `left open`), and the reason for anything left open, with links
- the baseline-repair PRs and what each fixed
- PRs that arrived during the run (from `NEW`) and what happened to them
- coverage notes: excluded repos, repos with no checkout, and any scan errors

For a dry run, replace the outcome column with the planned action and the
diagnosis, and list the dispatch order and pairs.

Don't claim deployments succeeded. Merging only queues them. Say that
deployment status wasn't verified unless Harry asks for a follow-up. Keep
the run directory as the receipt. Durable lessons, like a fix that keeps
recurring across repos, belong in a separate Jarvis PR, not in this skill's
run state.
