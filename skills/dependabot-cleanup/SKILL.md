---
name: dependabot-cleanup
description: Merge every open Dependabot PR across Harry's harryt04/* GitHub repositories, fixing merge conflicts and failing CI in Treehouse worktrees first, and keep sweeping until no new Dependabot PRs appear during the session. Use for /dependabot-cleanup, "merge all my dependabot PRs", "clear out the dependency bumps", "dependabot is piling up", or a dry run of what such a sweep would do, even when the user doesn't say "skill". Not for application security reviews or advisory triage without merging (use security-review).
---

# Dependabot cleanup

The deliverable is that every Dependabot PR open when the skill starts, plus
every one that appears while it runs, ends up merged, or is reported with a
concrete reason it couldn't be. One coordinator (this session) scans,
diagnoses, picks the order, and hands groups of repositories to T3 worker
sessions. Each session fixes and merges its repositories' PRs in Treehouse
worktrees, following [the worker brief](references/worker-brief.md).

Sessions merge in their own repositories, not the coordinator. Merging one
bump usually conflicts the next one's lockfile, so each PR has to be fixed
against the freshly merged default branch right before it merges. That loop
needs an agent that can wait for CI, and only a top-level session can. See
[dispatch shapes](#dispatch-shapes) for why.

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

## GitHub account

On Harry's machine the active `gh` account can be `harryclozd`, which can't
merge in `harryt04/*`. Run every GitHub write (merge, PR create or edit) as
`GH_TOKEN=$(gh auth token -u harryt04) gh ...`. Never run `gh auth switch`,
because other sessions depend on the active account. Git pushes use the
`github-harryt04` SSH remote and need nothing extra. Put this rule in every
worker prompt.

## Dry run

When Harry asks for a dry run, preview, or plan, or passes `--dry-run`, stop
after step 3. Report the scan, the per-repo diagnosis, and the order you would
dispatch in. Read-only investigation is fine (PR diffs, CI logs, default-branch
runs, branch protection). Don't acquire worktrees, push, comment, or merge.

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

Each row also carries `local_path` and `missing_required_checks`:

- `local_path` is the sibling folder whose `origin` is the repository. Use it,
  not the catalog's folder hint. (On 2026-11-10 the hints `scaffolding` and
  `voicebridge` were stale; the folders were `personal-project-scaffolding`
  and `voice-bridge`.) The table prints `NO CHECKOUT` when nothing matches.
- `missing_required_checks` lists branch-protection checks that never report
  on the PR. See step 2.

## 2. Diagnose each repository before dispatching

Spend a few read-only minutes per repository so each worker starts from the
real problem:

- When several PRs in one repo fail the same check, read one failing log.
  They usually share a single cause, such as Prettier rejecting Dependabot's
  lockfile formatting, a broken default branch, or a missing secret. One
  baseline fix then clears every PR. The raw log prefixes every line with job,
  step, and timestamp, which hides the message from a plain `grep`. Strip them:

  ```sh
  gh run view <id> -R <repo> --log-failed \
    | sed -E 's/^([^\t]*\t){2}[^ ]+ //' \
    | grep -iE 'error|warn|fail|ERR_' | grep -v deprecated | head -20
  ```

- Check the default branch's latest CI run on the same workflow. If it fails
  too, the PRs aren't to blame.
- A non-empty `missing_required_checks` means the PRs stay `BLOCKED` even
  when every job passes. This usually happens after a workflow job is split or
  renamed. The fix is a baseline PR that adds a gate job with the required
  name, which `needs` every real job and fails unless all of them succeed.
  It needs no settings change and weakens nothing.
- `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION` names the package and its publish
  time. Record when the gate passes (publish time plus the configured age).
  Those PRs are `time-gated`, not broken.
- Note which PRs touch the same lockfile. They will cascade into conflicts
  as their neighbors merge.

Record the diagnosis per repo in the run directory. It goes into the worker
prompt.

## 3. Plan the dispatch

Confirm each repository's checkout from the scan's `local_path`. If a
repository has no local checkout, clone it as a sibling only when Harry
agrees; otherwise report it as blocked.

Order repositories so the cheap ones go first: all-`ready` repos, then
conflicts, then CI failures. Every merge into a Coolify-hosted app queues a
deployment. The server builds two at a time and cancels superseded builds of
the same app
([burst record](../../docs/research/coolify-deployment-burst-2026-11-09.md)),
so **at most two repositories may be merging at once** across the whole run.
One repo's back-to-back merges just supersede each other.

Group the repositories into worker sessions of **3–5 repositories each**.
Each session works through its repositories one at a time, so two sessions
running at once keep the two-repo cap. Balance the groups by expected effort,
not by PR count. A repository with major migrations, such as TypeScript or
test-runner majors, is worth as much as several Prettier-only repositories.
Put repositories that share a diagnosed cause in the same session, so the
session reuses its fix. With 8 repositories, that gives two sessions of four,
both started at once.

Propose a provider, model, and reasoning effort for each session in the plan
table, as a recommendation. Harry confirms or changes them before the first
launch. Different sessions may use different models.

In a dry run, stop here and report (see step 6 for the format).

## 4. Dispatch worker sessions

Use [the T3 session spawner](../t3-session-spawner/SKILL.md) for every launch,
and follow its confirmation, launch, and receipt rules. In short:

- Before the first launch, confirm the provider, model, and effort for each
  session. Ask whether this coordinator thread should auto-settle after
  dispatch or remain active, and suggest a descriptive thread name. Harry can
  pin the thread himself; never pin it for him.
- Launch each session with `t3_thread_launch` in the Jarvis project with
  `workspaceStrategy: {type: "root"}`. Give it a stable `clientRequestId`, such
  as `dependabot-cleanup-<run>-<group>`, and the confirmed `modelSelection`.
  Keep receipts in the run directory.
- Don't link worker PRs to the coordinator thread. A linked PR's merge can
  settle the thread.

Each session prompt must work in a fresh session with no access to this chat.
It contains:

- the full text of [references/worker-brief.md](references/worker-brief.md)
- for each repository, in the planned order: the verified identity, default
  branch, `local_path`, the PRs as JSON from the scan (number, URL, head
  branch, state, failing checks), and your step 2 diagnosis
- the authority and GitHub account sections above, verbatim
- the exact baseline-repair PR title and branch from the brief, so every
  session's PRs look the same
- where to write the per-repo report: the run directory on the coordinator
  machine, or the report text in its final message when the session runs on
  another machine

Inside a session, the session agent owns the CI waits and merges for its
repositories. It may use native subagents to prepare the next repository in
parallel (read instructions, take its Treehouse lease, run the baseline
checks, draft the baseline fix). It merges one repository at a time.

If a session reports a cause that applies to other repos (the same Prettier
lockfile problem in several Next.js repos, say), message the sessions still
running and add it to the prompts for sessions not yet launched.

### Dispatch shapes

Use worker sessions by default. Use another shape only when Harry asks for it,
and keep its limits in mind:

- **Worker sessions (default).** A top-level T3 session can wait for CI with
  `watch_pull_request` and resume when checks finish. It runs the whole
  fix → push → wait → merge loop itself.
- **`delegate_task` children or native subagents.** On 2026-11-10, children
  followed the host rule that forbids PR waits. Two of three Codex
  (`gpt-6.1-sol`, low effort) children stopped after the first push, even when
  told to wait. A Claude Opus child waited and finished its repository alone,
  so the result depends on the model. The coordinator then
  had to watch each PR, merge it, and refresh the next one itself. If Harry asks
  for this shape, scope each child to setup and the baseline PR. Then run the
  per-PR loop in the coordinator with `watch_pull_request` and
  [scripts/refresh-pnpm-pr.sh](scripts/refresh-pnpm-pr.sh). Every PR costs one
  coordinator round trip, and the coordinator becomes the bottleneck.

## 5. Rescan until quiet

After each session finishes, rescan with the same `--seen` file. PRs marked
`NEW` appeared during the run: Dependabot often opens follow-ups or recreated
PRs after merges. Plan for this. On 2026-11-10 the first 46 PRs drew 20
follow-ups within an hour, then 8 more. They brought the same few bumps (next,
zod, dompurify, source-map-js) to repos that had just been cleared. Each wave
was smaller, and most of its PRs were already green. Those PRs still need a
refresh, because they are usually behind the default branch. Hand repositories with new or still-actionable PRs to a
session that is still running, or launch a new one. Then rescan again.

Sessions report `time-gated` PRs with the time they should pass. If that time
falls within the session, the session handles them itself. Otherwise report
the gate time so Harry can rerun the skill later.

Stop when a full scan has no `NEW` PRs and every remaining PR has a reported
reason, or after a third pass that makes no progress. Before stopping, wait
about two minutes and scan once more. Dependabot reacts to merges
asynchronously, and this final scan catches the PRs it opens late.

## 6. Report

Return:

- one table: repo, PR, title, outcome (`merged`, `fixed+merged`,
  `time-gated`, `superseded`, `left open`), and the reason for anything left
  open, with links
- the baseline-repair PRs and what each fixed
- PRs that arrived during the run (from `NEW`) and what happened to them
- any PR whose merged version differs from Dependabot's target (see the
  brief's lockfile rule)
- coverage notes: excluded repos, repos with no checkout, and any scan errors
- the worker session links and the Treehouse leases left in place

For a dry run, replace the outcome column with the planned action and the
diagnosis. List the session groups, their order, and the proposed model and
effort for each.

Don't claim deployments succeeded. Merging only queues them. Say that
deployment status wasn't verified unless Harry asks for a follow-up. Keep
the run directory as the receipt. Durable lessons, like a fix that keeps
recurring across repos, belong in a separate Jarvis PR, not in this skill's
run state.
