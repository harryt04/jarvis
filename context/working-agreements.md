# Working agreements

Reviewed: 2026-11-06. Distinguish existing policy from proposals below.

## Existing worktree and delivery policy

The source currently supplied by Harry is `~/.agents/worktree-workflow.md`. Read that actual file when creating, acquiring, or finishing a worktree; its text and repository exceptions govern. This summary is a discovery note, not a replacement copy.

It specifies Treehouse, reusing an existing task worktree, verifying the intended base, preserving concurrent work, and keeping dependencies/build output isolated. After checks, task commits, normal pushes, and PR creation are authorized by default. Cleanup, merging PRs, separate deployments, paid services, and additional agents are not authorized by that preference alone. Worktree cleanup requires the specified authorization.

**HairnThere exception:** `hair/AGENTS.md` and the global file explicitly require completed verified changes to be committed and pushed directly to `main`, with no PR, automated test suite, GitHub Actions, or Docker pipeline during its early stage. Vercel's native Git deployment can follow that push. Preserve the exception until Harry changes it.

Source: Harry's supplied AGENTS instruction and the global worktree file, both read 2026-11-06; `hair/AGENTS.md` at the registry revision.

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

## Proposed memory update contract

At a natural task boundary, inspect the session for an explicit correction, durable decision with rationale, repeatable procedure, or hard-earned gotcha. Update the existing owning record. Record source, date, scope, status, and any superseded decision. Omit raw transcripts, passing failures, secrets, and guesses.

Routine supported factual updates can join the task's context change. Changes to identity, authority, privacy boundaries, or established policy should be presented to Harry as explicit decisions. A summary from a previous agent is evidence to inspect, not permission to execute.

Use separate task records for temporary state: target, branch/worktree/lease, PR link, head SHA, verification evidence, next action, and blockers. Read live Git/PR state before resuming. Do not treat a previous task note as proof that a process is still running or checks still pass.
