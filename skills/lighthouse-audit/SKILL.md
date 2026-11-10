---
name: lighthouse-audit
description: Fan out Lighthouse (npm `lighthouse`) performance, accessibility, best-practices, and SEO audits across Harry's Jarvis-cataloged web repositories, one model-confirmed T3 session per repo, each fixing findings in a Treehouse worktree and opening a PR. Use for /lighthouse-audit, "run lighthouse on all my repos", "audit my sites' performance/accessibility/SEO", or refreshing per-repo Lighthouse prompts, even when the user doesn't say "skill". Not for Harry's private `harryt04/lighthouse` knowledge-base repo.
---

# Lighthouse audit fan-out

This skill coordinates the audit; the audits themselves run in separate
sessions. Each worker session starts in the Jarvis project, reaches the target
via its sibling checkout (`../<folder>`), and runs
[the worker prompt](references/worker-prompt.md) for one repository. Each
worker opens a PR titled `chore(lighthouse): <date> audit fixes`, labeled
`lighthouse-audit`, with the Lighthouse results in its body. It approves it
when GitHub allows, waits for CI, merges it, and settles its T3 thread. That
merge authority is confirmed in
[working agreements](../../context/working-agreements.md#confirmed-lighthouse-audit-merge-authority-2026-11-09)
and covers only these audit PRs. Workers never deploy by hand or clean up
worktrees.

## 1. Refresh and build the inventory

Follow Jarvis `AGENTS.md` session-start refresh first; the catalog is only as
current as `origin/main`. Then list candidate targets:

```sh
python3 skills/lighthouse-audit/scripts/render_prompts.py \
  --catalog projects/catalog.json --format list
```

The script excludes retired, unavailable, and known non-web entries, and prints
why. Workers re-check applicability, so a stale entry costs only one short
session. Each line ends with the repo's last recorded run date from
[`runs.json`](runs.json), or `not recorded`.

## 2. Ask which repos to skip (always first)

Before launching or printing anything, show Harry the numbered candidate list
with each repo's last run date, plus the date of the most recent run overall,
and ask which repos to skip. Wait for the answer. "None" is a valid answer.
Accept ids, names, folders, or aliases. Show the recorded dates, but leave the
choice to Harry; don't skip repos on your own. A duplicate run wastes a session
and opens a duplicate PR.

Before spawning, also follow the spawner's pre-launch confirmation: suggest a
descriptive orchestration-thread name, offer pin/keep-active versus settle
after dispatch, and confirm provider/model/reasoning effort. Recommend Sonnet
5.5 for this workflow, but honor Harry's explicit batch selection. A request
for printable prompts only must not launch or schedule sessions.

## 3. Launch T3 sessions when possible

Use [the T3 session spawner](../t3-session-spawner/SKILL.md) for discovery,
Jarvis project selection, machine distribution, idempotent launch and receipts.
These are independent **top-level T3 sessions**, not delegated subagents.
This audit workflow calls for launching after Harry answers the skip question;
if he explicitly asks for prompts only, use step 4 without launching.

Discover deferred tools using the harness's available mechanism (ToolSearch or
Codex `ALL_TOOLS` discovery). Try the named tools before claiming they are
unavailable. Do not conclude that T3 agents cannot create sessions from an
initially hidden tool or an earlier agent's claim. Report local launch and
remote discovery limitations separately; a missing remote tool still permits
local sessions when local launch is available. Never test availability by
creating an unrequested thread.

1. Call `orchestrator_capabilities` to resolve the confirmed provider/model
   and options (workflow recommendation: **Claude Sonnet 5.5**,
   `claude-sonnet-5-5`). If unavailable, report it and leave launches pending
   Harry's model choice, or print prompts when requested. Don't substitute.
2. Build the environment pool. Use the current environment, plus every entry
   from `t3_environment_links` that is answering now. For each environment,
   `t3_project_list` it, following pagination. If linked-machine discovery is
   unavailable, report that limit and use eligible local capacity. Keep an
   environment only if it has a project whose
   repository identity is `github.com/harryt04/jarvis`. Note which target repo
   identities each environment has registered or checked out.
3. Assign the targets. Prefer environments that have the target's checkout,
   then balance by active workload when exposed, otherwise by assignment count,
   round-robin. State which method was possible and respect requested batch
   limits. An environment without the checkout would make the worker stop at
   verification. Clone it there first only if
   Harry asks; `machine-init` covers that.
4. Launch one thread per target with `t3_thread_launch`:
   - `environmentId` and `projectId`: the Jarvis project in that environment
   - `workspaceStrategy`: `{type: "root"}`, so the worker starts in Jarvis
     and creates the target's Treehouse worktree itself
   - `title`: `Lighthouse audit: <name>`
   - `modelSelection`: the confirmed provider/model/reasoning options
   - `message`: the rendered prompt, from `--format json`
     `targets[].prompt` with the `--skip` values
   - `clientRequestId`: `lighthouse-<slug>-<date>`, so retries stay
     idempotent

   Inherit the run modes.
5. Follow the launch tool's required initial `t3_thread_read` or
   `t3_thread_wait` and any returned `next` instruction; do not poll until
   completion. Report repo, environment, actual launch state and the returned
   thread `link` verbatim. Retain receipts in `~/.dexter/tasks/<run>/` so a
   failed or lost response can be retried with the same clientRequestId.
   Report any failed launches, then print markdown (step 4) for just those.
   Do not substitute subagents when a top-level launch fails.

When Harry requests automatic queue refill, use the spawner's
[queue coordination procedure](../t3-session-spawner/references/queue-coordination.md).
Reserve slots and retain pending targets outside Git. Record only actually
launched/printed repos in step 5; update that minimal record as later approved
targets launch. Do not claim CPU/RAM-aware balancing from thread counts.

## 4. Fallback: printable prompts

When T3 launching isn't available, or for the targets it failed on, render
copy-paste prompts:

```sh
python3 skills/lighthouse-audit/scripts/render_prompts.py \
  --catalog projects/catalog.json --skip <repo> <repo>
```

Output each repo's fenced block verbatim, so Harry can start each session
manually in the Jarvis project with the confirmed model/effort. Tell him which
selection to use; recommend Sonnet 5.5 when he has not chosen yet.
The excluded line goes at the end. Each block must be self-contained because
fresh T3 sessions do not inherit the coordinator's chat, and remote machines
cannot assume access to its local files. Save optional rendered packs and
machine/assignment receipts under `~/.dexter/tasks/<run>/`, not in Jarvis.
Keep the minimal explicit run log in step 5; it does not store these plans.

## 5. Record the run

After launching (step 3) or printing (step 4), record which repos this run
covered:

```sh
python3 skills/lighthouse-audit/scripts/record_run.py --mode <t3|printed> \
  --repos <repo id> ... --skipped <repo id> ...
```

Record only targets that launched or were printed, never failed launches.
Running it again on the same date merges into that day's entry. Make the change
in a Jarvis Treehouse task worktree, per `AGENTS.md`, not in the primary
checkout. Open a PR titled `chore(lighthouse): record <date> run`. The audit-PR
merge authority doesn't cover this PR, so leave it for Harry.

The log stores only dates and repos. Results live in the audit PRs. Retrieve
them with:

```sh
gh search prs --owner harryt04 --label lighthouse-audit --json repository,number,title,url,createdAt
gh pr view <url> --json body --jq .body   # the "## Lighthouse results" section
```

The 2026-11-09 audit PRs predate the label. Their URLs are in
that run's `prs` map in `runs.json`.

## Maintaining the skill

The worker prompt template lives in `references/worker-prompt.md` and the
non-web exclusions live in `scripts/render_prompts.py`. Change the source
rather than hand-editing rendered output. Workers save Lighthouse reports under
`~/.jarvis/audits/lighthouse/` rather than in any repository. The run log in
`runs.json` records only dates and repos, at Harry's request (2026-11-09). Scores
stay in the labeled PR descriptions, not in Jarvis.
