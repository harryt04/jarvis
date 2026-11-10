---
name: lighthouse-audit
description: Fan out Lighthouse (npm `lighthouse`) performance, accessibility, best-practices, and SEO audits across Harry's Jarvis-cataloged web repositories, one Sonnet 5.5 session per repo, each fixing findings in a Treehouse worktree and opening a PR. Use for /lighthouse-audit, "run lighthouse on all my repos", "audit my sites' performance/accessibility/SEO", or refreshing per-repo Lighthouse prompts, even when the user doesn't say "skill". Not for Harry's private `harryt04/lighthouse` knowledge-base repo.
---

# Lighthouse audit fan-out

This skill coordinates the audit; the audits themselves run in separate
sessions. Each worker session starts in the Jarvis project, reaches the target
via its sibling checkout (`../<folder>`), and runs
[the worker prompt](references/worker-prompt.md) for one repository. Each
worker opens a PR titled `chore(lighthouse): <date> audit fixes`, approves it
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
session.

## 2. Ask which repos to skip (always first)

Before launching or printing anything, show Harry the numbered candidate list
and ask which repos to skip, for example ones audited recently. Wait for the
answer. "None" is a valid answer. Accept ids, names, folders, or aliases. Don't
infer recency from old PRs yourself. The question exists because Harry tracks
what he ran recently, and a duplicate run wastes a session and opens a
duplicate PR.

## 3. Launch T3 sessions when possible

Try automatic launching when T3 tools are present. Load them with ToolSearch
first, since they may be deferred.

1. Call `orchestrator_capabilities` to find the provider and model selection
   for **Claude Sonnet 5.5** (`claude-sonnet-5-5`). If it isn't offered, say so
   and fall back to step 4. Don't substitute another model unasked.
2. Build the environment pool. Use the current environment, plus every entry
   from `t3_environment_links` that is answering now. For each environment,
   `t3_project_list` it. Keep an environment only if it has a project whose
   repository identity is `github.com/harryt04/jarvis`. Note which target repo
   identities each environment has registered or checked out.
3. Assign the targets. Prefer environments that have the target's checkout,
   then balance by count, round-robin. An environment without the checkout
   would make the worker stop at verification. Clone it there first only if
   Harry asks; `machine-init` covers that.
4. Launch one thread per target with `t3_thread_launch`:
   - `environmentId` and `projectId`: the Jarvis project in that environment
   - `workspaceStrategy`: `{type: "root"}`, so the worker starts in Jarvis
     and creates the target's Treehouse worktree itself
   - `title`: `Lighthouse audit: <name>`
   - `modelSelection`: Sonnet 5.5
   - `message`: the rendered prompt, from `--format json`
     `targets[].prompt` with the `--skip` values
   - `clientRequestId`: `lighthouse-<slug>-<date>`, so retries stay
     idempotent

   Inherit the run modes.
5. Don't wait on or poll the threads. Report a table of repo, environment, and
   the thread `link` exactly as returned. Report any failed launches, then
   print markdown (step 4) for just those.

## 4. Fallback: printable prompts

When T3 launching isn't available, or for the targets it failed on, render
copy-paste prompts:

```sh
python3 skills/lighthouse-audit/scripts/render_prompts.py \
  --catalog projects/catalog.json --skip <repo> <repo>
```

Output each repo's fenced block verbatim, so Harry can start each session
manually in the Jarvis project with Sonnet 5.5. Tell him which model to select.
The excluded line goes at the end.

## Maintaining the skill

The worker prompt template lives in `references/worker-prompt.md` and the
non-web exclusions live in `scripts/render_prompts.py`. Change the source
rather than hand-editing rendered output. Workers save Lighthouse reports under
`~/.jarvis/audits/lighthouse/` rather than in any repository. Dated results and
PR links are task state, not portable Jarvis memory.
