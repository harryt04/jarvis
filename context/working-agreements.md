# Working agreements

Reviewed: 2026-11-09. Distinguish existing policy from proposals below.

## Confirmed session refresh, worktree, and PR policy, 2026-11-09

At every new Jarvis session, fetch and load the latest verified `origin/main`
from Jarvis before relying on memory, including when the task targets another
repository. Preserve dirty checkouts and existing task history; use the safe
[session refresh procedure](../docs/treehouse-workflow.md#session-start-refresh).
Re-read the refreshed entry point and context rather than relying on startup
text already loaded by the harness. Disclose fetch failures and stale context.

For Jarvis and all other code repositories, always use Treehouse-managed task
worktrees and submit a PR when done. Reuse an existing task worktree when
appropriate. Install Treehouse if absent using the
[portable runbook](../docs/treehouse-workflow.md), which also owns command and
base-selection guidance. Apply this policy to any separately authorized
subagents or delegated agents and include it in their task instructions.

Source: Harry's explicit Jarvis instruction, 2026-11-09. Scope: permanent,
cross-machine session startup and repository work. This strengthens the
2026-11-07 Treehouse default and supersedes its fallback allowance and the
historical HairnThere direct-main/no-PR exception. Other project verification
rules remain scoped to their repositories. Existing machine workflow files
may supplement this portable policy but cannot silently restore the older
exception. Task commits, ordinary pushes, and PR creation are authorized;
this grants no blanket merge, deployment, cleanup, or delegation authority.

## Confirmed Lighthouse audit merge authority, 2026-11-09

Workers started by the [lighthouse-audit skill](../skills/lighthouse-audit/SKILL.md)
may approve their own audit PR when GitHub allows it. They wait for PR CI where
it applies, then merge the PR once checks pass and the branch is mergeable. This
covers only PRs titled `chore(lighthouse): <date> audit fixes` that the worker
opened in its task, and only with the repository's allowed merge methods,
without admin overrides or bypassing protections. After merging, or when no PR
is needed, a worker running in T3 settles its own thread.

Source: Harry's explicit Jarvis instruction, 2026-11-09. Scope: Lighthouse
audit workers only. Merging may trigger a repository's existing automatic
deployment. This grants no authority to start or change deployments, merge
other PRs, or clean up worktrees.

## Confirmed Dependabot cleanup merge authority, 2026-11-10

During a run of the [dependabot-cleanup skill](../skills/dependabot-cleanup/SKILL.md),
the coordinator and its per-repository workers may merge open
Dependabot-authored PRs in live, non-archived `harryt04/*` repositories. That
includes major-version bumps and PRs that were open at invocation or opened
during the run. Before merging, they may resolve conflicts and fix failing
checks by pushing normal (non-force) commits to the Dependabot branch from a
Treehouse task worktree. They may also open and merge a minimal PR titled
`fix(ci): repair checks for dependabot cleanup` when a default branch's own
checks block those PRs. Merges require passing PR checks (or, for a repository
without CI, passing local checks on the exact head) and a mergeable branch,
using an allowed merge method pinned to the validated head, without admin
overrides, bypassed protections, or weakened checks.

Source: Harry's explicit Jarvis instruction, 2026-11-10. Scope: dependabot-cleanup
runs only. Merging may trigger a repository's existing automatic deployment.
This grants no authority to close Dependabot PRs, dismiss alerts, start or change
deployments or hosting settings, merge other PRs, or clean up worktrees.

## Confirmed Treehouse cleanup authority, 2026-11-10

Under the [treehouse-cleanup skill](../skills/treehouse-cleanup/SKILL.md), any
agent may reclaim Treehouse slots on Harry's machines without asking, when pools
are full or Harry asks. A slot qualifies only when its tree is clean, a GitHub
PR for its branch is merged, no PR for it is open, and its local HEAD is
contained in the merged PR head. Reclaiming means terminating processes whose
working directory is inside that slot (SIGTERM, then SIGKILL) and running
`treehouse return <path> --if-lease-id <id>` without `--force`.

Source: Harry's explicit Jarvis instruction, 2026-11-10. Scope: merged slots
only. This grants no authority to touch unmerged, open, closed-unmerged, dirty,
or unverifiable slots or their processes, run `destroy` or `--force`, kill
processes outside a reclaimable slot, or merge or deploy anything.

## Proposed general delivery standard

Use this as the migration plan, not newly granted permission:

1. Inspect the target's actual instructions, branch, remote, worktrees, existing changes, and installed tooling.
2. Work in a task branch and isolated checkout under the applicable Treehouse policy; explicitly choose the current default base.
3. Run the target's real checks. Record failures and unavailable configuration accurately. Add tests appropriate to behavior and risk, subject to explicit repository exceptions.
4. Keep one coherent change per PR; include what changed, why, validation, and material limits. Update affected documentation with the change.
5. Keep merges and production promotion under explicit authority. PR previews and isolated test data can provide review without maintaining permanent dev/beta/prod branches for every small app.
6. Protect default branches and require meaningful checks per repository after reviewing its deployment and contributor needs. Verify GitHub support for the repository/account before changing protection settings.

For Jarvis itself, use a lightweight documentation check (links, registry consistency, accidental secrets, and diff review). Do not make application builds or a large test platform a prerequisite to correcting a memory.

## Source ownership

- Jarvis owns Harry's portable preferences, cross-project context, project routing, and transferable lessons.
- Each target repository owns its product specification, architecture, commands, and detailed gotchas. Jarvis stores a brief and pointers, not a second full specification.
- `harryt04/agent-skills` already owns Harry's shared skill collection. Inventory and reference it before copying or adding skills.
- Machine-local context may supply paths and capabilities. It cannot silently enlarge authorization or override confirmed portable preferences.

## Confirmed memory-request delivery, 2026-11-07

When Harry says "update Jarvis's memory," persist the understanding in the
owning long-term repository record and create or update a pull request. For
portable personal and cross-project context, that repository is Jarvis. A
machine-local note or chat acknowledgement alone does not fulfill the request.
The result must travel across machines, providers, and sessions after the PR
merges. Link the PR in the response; merging still follows the applicable
explicit authority rather than being inferred from a memory-update request.

Source: Harry's explicit clarification in the Jarvis conversation, 2026-11-07.
This confirmed delivery requirement supersedes the proposed contract below
where that proposal would allow a memory request to end without a PR.

## Proposed memory update contract

At a natural task boundary, inspect the session for an explicit correction, durable decision with rationale, repeatable procedure, or hard-earned gotcha. Update the existing owning record. Record source, date, scope, status, and any superseded decision. Omit raw transcripts, passing failures, secrets, and guesses.

Routine supported factual updates can join the task's context change. Changes to identity, authority, privacy boundaries, or established policy should be presented to Harry as explicit decisions. A summary from a previous agent is evidence to inspect, not permission to execute.

Use separate task records for temporary state: target, branch/worktree/lease, PR link, head SHA, verification evidence, next action, and blockers. Read live Git/PR state before resuming. Do not treat a previous task note as proof that a process is still running or checks still pass.
