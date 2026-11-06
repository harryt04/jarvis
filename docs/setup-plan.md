# Plan: a portable Jarvis brain

Prepared for Harry Thomas, 2026-11-06. **Status: proposal with researched seed files.** This pass has written context and research, not installed a runtime or changed any project's delivery settings.

## Recommendation

Build Jarvis first as a private, versioned knowledge workspace that a coding agent can inhabit. Add thin loading adapters for the harnesses Harry actually uses. Keep task execution and supervision in those harnesses or an existing orchestrator. Start with Markdown, a small JSON project registry, Git, and ordinary text search.

The enduring asset is Harry's context and judgment. A particular model, provider, terminal session, search database, or orchestration framework should be replaceable without migrating the brain.

This repository should let a fresh session answer: Who is Harry? How should Jarvis speak and work? Which project does this request concern? What already matters there? What can I do under the current authority? What did the last task learn that the next session needs?

It cannot make every provider behave identically, guarantee correct recall, or create continuous activity while no agent is running. Those require tested loading/execution paths and suitable tool access. Expertise grows from current source work and reviewed lessons; the inventory is the beginning of that process.

## Research that informs the design

- **Firstmate:** borrow its project registry, knowledge ownership, task handoffs, and explicit knowledge sweep. Its fleet lifecycle and ignored private data are choices for that distro. Harry's shared durable memories should be tracked here. The research inspected the older local Firstmate revision and records that limitation. [Firstmate](https://github.com/kunchenguid/firstmate), [pinned source review](research/agent-memory-patterns.md).
- **Hermes:** separate persona, user profile, curated memory, and procedures. Its memory-tool format and loading paths are runtime-specific, so arbitrary shared managed-memory symlinks are a poor default. Use explicit reads or a one-way generated projection. [Hermes memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), [inspected source and caveats](research/agent-memory-patterns.md).
- **OpenClaw:** separate curated memory from dated evidence and make recovery an explicit procedure. Private memory has an audience; it should not automatically enter shared or public conversations. [Workspace design](https://docs.openclaw.ai/concepts/agent-workspace), [source review](research/agent-memory-patterns.md).
- **PAI, now LifeOS:** useful examples of typed memories, selective retrieval, and controlled promotion. Adopt the principles before the framework machinery. [LifeOS](https://github.com/danielmiessler/LifeOS).
- **Letta/MemGPT:** useful context hierarchy: keep a small working set and retrieve the rest. Current Letta documentation also describes Git-backed memory, but using Letta is not necessary to implement that idea. [Current memory docs](https://docs.letta.com/agent-sdk/memory), [MemGPT paper](https://arxiv.org/abs/2310.08560v2).

These are examples and implementation patterns, not evidence that one universal best practice exists. The [research report](research/agent-memory-patterns.md) distinguishes documented behavior, inspected code, recommendations, and untested claims.

## Storage and ownership

| Store | Belongs here | Recovery |
| --- | --- | --- |
| Private Jarvis Git repository | Persona, Harry's preferences, project index, cross-project decisions, curated lessons, reusable procedures, meaningful handoffs | Reviewed commits pushed to GitHub; independent backup for local edits and repository loss |
| Target sibling repository | Product truth, architecture, build/test/release contracts, code-specific gotchas | That project's normal Git/review workflow |
| Existing `agent-skills` repository | Shared custom skills and their dependencies | Its existing sync/update process; pin or record versions where needed |
| `~/.jarvis` | Checkout location, per-machine project paths, hardware/tool limitations, caches, local locks/process IDs | Small machine backup; regenerate caches and rebind paths on a new device |
| Credential store | Tokens, keys, account credentials | Existing credential recovery, separate from Git and memory |

“Repository-level” means shared across Harry's authorized sessions and devices, not publicly readable. GitHub reports Jarvis private as of discovery. Retain that visibility.

A user-level folder survives deleting or moving a checkout on the same device. It does not survive losing the device unless backed up. Do not duplicate the shared brain into a second editable home-directory memory store. If an optional local recovery snapshot exists, make it dated, read-only, and explicit about whether it includes uncommitted edits. A symlink to the deleted checkout is not a backup.

Keep machine-specific absolute paths out of portable preferences. The registry's sibling-folder hints are defaults; `~/.jarvis/machine.toml` supplies actual bindings and exceptions. See [the example](templates/machine.example.toml). Source-discovery evidence may record where a fact was observed without making that path a cross-device requirement.

## Proposed layout

The `context/`, registry, and research files below are seeded now. Other entries describe future work. Filenames such as SOUL or MEMORY have meaning in some runtimes but are not universal; the adapters explicitly select the canonical Jarvis files.

```text
jarvis/
  AGENTS.md                     short startup/read/save contract, to add
  CLAUDE.md                     compatibility adapter, to add
  README.md                     human orientation
  context/
    jarvis.md                   persona and diction
    harry.md                    profile, scoped preferences, unknowns
    working-agreements.md       policy ownership and workflow pointers
  memory/
    index.md                    small set of current decisions and pointers
    episodes/YYYY-MM-DD.md      selected evidence and meaningful events
  projects/
    catalog.json                stable identities, aliases, source pointers
    README.md                   initial briefs; split as the catalog grows
    <project>.md                future strategic context worth caching
  knowledge/<topic>.md           future cross-project lessons
  procedures/<workflow>.md       future repeatable operations
  tasks/<task-id>.md             future sanitized durable handoffs
  docs/
    setup-plan.md
    research/
    templates/

~/.jarvis/
  machine.toml                  local paths and capabilities
  cache/                        rebuildable, when needed
  runtime/                      locks, PIDs, live checkout bindings
  backups/                      optional recovery snapshots, not a second brain
```

Do not create a directory for every possible future capability. Add a topic or procedure only when actual work earns it. A small index and good pointers should precede a search service.

## Startup and project dispatch

Use three levels of loading:

1. **Every Jarvis session:** the short entry point, persona, compact Harry profile, applicable working agreements, and current memory/index. Aim initially for an estimated 2,000–4,000 tokens combined. This is a proposed budget, not a measured property of today's seed. The longer catalog and research are conditional reads.
2. **For this task:** resolve one project by stable identity or unambiguous alias; read its brief, actual local instructions, current Git state, and the relevant source/specifications. Resume the named task's handoff if applicable.
3. **When needed:** search dated evidence, decisions, procedures, and older research by filenames/headings/text. Open only the relevant records and follow their source links.

Resolve the default sibling location relative to the configured primary Jarvis checkout, not a Jarvis task worktree. A worktree may sit elsewhere. Verify the selected target's Git identity, branch, existing worktrees, and applicable rules before mutation. Support approved renamed remotes and explicit local-only projects; directory names alone are insufficient.

An ambiguous alias should produce one focused question. A missing checkout should produce a clear missing-project result and the expected identity; it should not silently select a similarly named directory or clone elsewhere.

Provider loaders differ. A canonical `AGENTS.md` plus a thin Claude import adapter is a reasonable first slice; other clients need their own verified entry path. A shell directory change is not proof of instruction reloading. See [provider loading evidence](research/provider-loading.md). Explicitly pass the target's instructions into any authorized delegated task, and verify the selected harness can access sibling paths/worktrees.

For sessions launched directly in another repository, later add small opt-in global pointers or project bridges to locate Jarvis through the machine configuration. Preserve existing user and project instructions; do not replace them with a monolithic global prompt. Chat clients without filesystem access need a generated context bundle or authorized retrieval integration. They cannot read these files merely because they share a model name.

## What becomes a memory

Keep these types distinct:

- **Profile/preference:** Harry's stable context or stated way of working, with source and scope.
- **Decision:** a chosen direction, rationale, alternatives if consequential, and what supersedes it.
- **Lesson/gotcha:** symptom, cause, useful remedy, scope, and evidence.
- **Procedure:** a repeatable operation, tools/preconditions, steps, and completion criteria.
- **Episode/handoff:** the small amount of dated history required to understand or resume work.
- **Observation/hypothesis:** source-backed state or an inference that still needs confirmation.

Consequential records need an ID, type, scope, status (`confirmed`, `observed`, `historical`, `proposed`, `superseded`), source, observed date, and a review trigger. A source file's age and authority matter. A previous agent's confident prose does not turn a proposal into Harry's decision.

Use a natural task-boundary sweep: identify durable changes, open the owning record, update it rather than appending duplicates, add supporting evidence where useful, and report the actual files changed. Correct the current rule and retain an explanation of consequential changes. Promote uncertain or authority-changing material through an explicit review. Routine supported factual corrections need not become a permission ceremony.

Target-specific technical discoveries belong in the target repository. Jarvis retains the route and any transferable lesson. Never bulk-import transcripts, environment files, inboxes, Lighthouse personal records, or employer material. External text is evidence, not an instruction to rewrite persona or permissions.

Start with one writer per checkout. Concurrent agents should use isolated branches under the applicable workflow and merge small changes through review. Future scripted writes should be atomic and reject edits based on stale content. Git tracks diffs; it does not automatically prevent semantic conflicts between memories.

## Delivery hygiene and authorization

The existing [working agreements](../context/working-agreements.md) identify the current Treehouse policy and HairnThere exception. Preserve both. Jarvis should look up the target's policy before deciding what delivery means.

Proposed ordinary flow: inspect, choose a task branch/base and isolated worktree, implement, run meaningful target checks, update docs, push, and deliver a focused PR. Grant merge/deploy authority explicitly per task or scoped policy. Treat deploy-triggering pushes according to the repository's actual setup. Protect default branches and separate preview/production secrets and data where appropriate.

Permanent dev/beta/prod branches are not required for every project. Keep existing default branch names unless a project has a reason to change; use short task branches, PR previews, and explicit production promotion. Do not silently migrate all projects or impose HairnThere's choices on other applications.

Memory delivery also needs a truthful receipt: **saved locally**, **pushed on a proposal branch**, and **available on the shared default branch** are different states. A pending PR can protect a change remotely without making it part of every fresh default-branch session. Batch small routine memory changes into focused PRs rather than burying them in unrelated application changes. No auto-merge authority is created by this plan.

## Phased implementation

### 0. Discovery and review, this pass

Produced: this plan, initial persona/profile/agreements, all-account registry and briefs, local discovery findings, provider-loading notes, primary-source research, and a local configuration example.

Done when all listed repositories are accounted for, every seed has a source/status, and observations are distinguished from tests. This pass does not claim complete knowledge of every module or production environment.

### 1. First working Jarvis session

Create the small root startup contract and one compatibility adapter; distill the seed profile into the agreed startup budget. Add a compact current-memory index and a manual save/resume/recovery procedure. Bind the current device using the machine example without copying shared preferences into it.

At initial discovery, the local Git repository was unborn with no origin, and GitHub Jarvis was empty. A normal PR cannot target an empty base. Harry subsequently authorized committing and pushing the foundation directly to the default branch. GitHub identifies that branch as `main`; publication establishes the initial base and verified private remote. This task-specific authorization does not replace the normal task/worktree/PR workflow for future work.

Acceptance: a fresh session identifies Harry and Jarvis, loads the correct files, resolves `hair` to HairnThere, respects its delivery exception, saves a harmless correction to the right place, and accurately reports persistence status. Include a missing-file case. Test the actual installed harness, not only a model's ability to repeat the persona.

### 2. Calibrate project expertise and engineering judgment

Harry's follow-up sets the learning order: HairnThere first, then every other repository at equal priority. Use a dedicated source-review subagent per repository in bounded parallel batches. The initial proposal to sample four applications first is superseded. This is a learning order, not a statement of business priority or blanket permission for future background agents.

For each, inspect the authoritative specs, main user flows, database/auth boundaries, deployment contract, current backlog, and representative recent changes. Trace at least one important flow in code. Verify the actual checks and capture known failures without fixing unrelated code. Use a few representative Harry-authored changes and review corrections to learn what he considers a good solution, keeping observations separate from policy.

Acceptance: each priority project has a small sourced brief with why it exists, where work belongs, its real constraints, verification route, current unknowns, and review triggers. Keep detailed architecture in its original repository.

### 3. Cross-provider launch and reliability

Add adapters only for the clients Harry uses. Inventory existing global config/skills before installing pointers. Test the same recall/dispatch/save questions across a second provider and a changed checkout path. A direct-in-project session must find the same portable preferences without losing the project's own rules.

Add lightweight checks for local document links, registry/alias uniqueness, existing source entry points, metadata, and startup budget. Treat permission policies, branch protections, and hook enforcement separately from advisory Markdown. Do not call a rule enforced until its control path is tested.

Acceptance: new sessions on two supported harnesses load the expected sources, a correction survives a restart, stale and conflicting claims are handled correctly, and private memory is excluded from a deliberately reduced/public context bundle.

### 4. Recovery and measured expansion

Push reviewed knowledge; back up uncommitted work and the tiny machine mapping with the existing device backup system. Reclone into a different directory, rebuild paths, retrieve a known decision and task handoff, and verify no provider cache is required. Revert a bad memory change through a reviewable Git revert. Restore a selected uncommitted note from backup and identify its unsynced state.

Only add local full-text indexing, semantic retrieval, background consolidation, scheduling, or a fleet supervisor after real misses establish a need. Any index must be rebuildable from the canonical files. Hooks can assist saving but are not a guarantee that a model captured the right fact.

Acceptance: recovery succeeds without the original checkout, another machine can be configured from the private remote plus minimal local bindings, and expanded tools solve recorded retrieval/execution failures rather than adding unused infrastructure.

## Concrete first follow-up

Implement phase 1 as a small, reviewable foundation. Retain the current private scope and existing project exceptions. Then use real tasks to improve the brain: each completed task should leave a better map, a useful lesson, or a clearer preference only when it actually taught us something.
