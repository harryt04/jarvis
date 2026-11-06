# Agent memory patterns for Jarvis

Researched 2026-11-06. Scope: primary-source research and read-only local inspection; no installation or runtime trials. **Recommendation:** make this private repository the canonical, provider-neutral Markdown brain; keep startup context small, retrieve project and historical detail on demand, and put only machine bindings in `~/.jarvis`. Start with files, Git, and `rg`, not a vector database or background service.

Harry-specific context below comes from the task brief, not external verification: Harry Thomas owns `harryt04/*`, works as a staff SWE at Clozd, keeps repositories under `~/Documents/git/*`, has historically used main/master directly, and wants stronger agent hygiene. “Shared” here means shared across Harry's authorized machines and tools, not published or automatically shared with coworkers.

## Evidence and revision ledger

All sources accessed 2026-11-06. Commit timestamps below are upstream committer dates, not test dates. Source links in the findings pin inspected code where possible.

- **Firstmate local checkout:** `../firstmate`, HEAD `cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e`, 2026-08-02. Read README, AGENTS, configuration, public/internal stow, startup-budget helper, and the stow verification record. No Firstmate command was executed. GitHub main was separately observed at `bf05a4fcd69b8bb27f261177eac4abb57f98aa1b`, 2026-11-06; its implementation was **not** audited. Findings describe the older local checkout, not current main. [Inspected revision](https://github.com/kunchenguid/firstmate/tree/cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e).
- **NousResearch Hermes Agent:** main `6b21d0564de0492e2ebd0d8f63fca86c03b5c892`, 2026-11-06. Read pinned memory, skills, context-file and SOUL docs, plus `tools/memory_tool_store.py`; live official docs were also consulted. [Revision](https://github.com/NousResearch/hermes-agent/tree/6b21d0564de0492e2ebd0d8f63fca86c03b5c892).
- **OpenClaw:** main `d482d761651209a65a84a2865137147b7802e1d3`, 2026-11-06. Read workspace/memory docs and relevant bootstrap/workspace source. [Revision](https://github.com/openclaw/openclaw/tree/d482d761651209a65a84a2865137147b7802e1d3).
- **Daniel Miessler PAI:** the requested `danielmiessler/PAI` repository redirects to **LifeOS**. Inspected main `f6ab5e0228bfb356c82edbf52b69344dbd585486`, 2026-11-05: README, memory/skill documentation, LoadContext hook, CortexAdapter and MemorySystem source excerpts. Do not apply old PAI directory recipes blindly. [Revision](https://github.com/danielmiessler/LifeOS/tree/f6ab5e0228bfb356c82edbf52b69344dbd585486).
- **Letta:** current Agent SDK memory docs and explicitly labeled **V1 SDK (legacy)** memory-block/context-hierarchy/AgentFile docs; live pages have no inspected immutable revision. GitHub main metadata was observed at `8816d3a8516893bfdc0fa14bfb1235226012e295`, 2026-10-18, but that code was not inspected and is not evidence for the current SDK's implementation. [Current memory docs](https://docs.letta.com/agent-sdk/memory), [legacy hierarchy](https://docs.letta.com/v1-sdk/memory/context-hierarchy).
- **MemGPT paper:** arXiv `2310.08560v2`, revised 2024-02-12; inspected abstract/version record, not reproduced experiments. [Primary paper](https://arxiv.org/abs/2310.08560v2).

“Code-verified” means the relevant implementation was read, not that it was executed. “Documented” means an official source states the behavior. Recommendations are design proposals for Jarvis, not existing Jarvis features.

## What the examples actually establish

### Firstmate: ownership, bounded startup memory, explicit dispatch

**Verified in the local source:** tracked instructions/tooling are separated from ignored private `data/`, volatile `state/`, and local `config/`. `data/projects.md` is a thin navigation registry. Knowledge routes to its most specific owner: captain preferences, fleet-local learnings, task records/research reports, project instructions, or distro-wide material. A project's durable contributor knowledge belongs with that project, rather than being copied wholesale into the fleet brain. [AGENTS §§2, 6](https://github.com/kunchenguid/firstmate/blob/cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e/AGENTS.md#6-project-and-knowledge-management).

Its internal stow procedure reads all startup memory, prioritizes current preferences and authority, rewrites/prunes stale entries, routes detail to stronger owners, and reports before/after size. This is a **curation procedure expressed as agent instructions**. The public standalone stow is different: discover the host's conventions, prefer explicit destinations, and use a private local fallback if needed; an issue tracker is not inferred merely from an existing remote. [Internal stow](https://github.com/kunchenguid/firstmate/blob/cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e/.agents/skills/stow/SKILL.md), [public stow](https://github.com/kunchenguid/firstmate/blob/cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e/skills/stow/SKILL.md).

**Enforcement distinction:** the budget helper validates inputs and reports estimated tokens using `ceil(UTF-8 bytes / 3)`. An over-budget report prints `budget_status=over-budget` but does not itself fail the command or prevent future edits. The skill tells the agent not to call an over-budget session reset-safe. Likewise, the session-start contract tells the agent to invoke the startup script; native adapters are described as nudges. These are not universal guarantees that every provider loaded or obeyed the material. [Budget implementation](https://github.com/kunchenguid/firstmate/blob/cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e/bin/fm-startup-memory-budget.sh), [startup contract](https://github.com/kunchenguid/firstmate/blob/cd73e75e02a1c1e74811b00c5ee08ffae8a59e1e/AGENTS.md#3-session-start-run-once-at-every-session-start).

**Jarvis implication:** borrow ownership routing, compact receipts, and a small project registry. Do not copy Firstmate's ignored-private-data split: Harry wants durable personal memory versioned and synchronized. Its fleet/watchers/secondmates are a separate operational system, unnecessary for the initial brain.

### Hermes: persona, profile, notes, and skills are distinct surfaces

**Documented and partly code-verified:** `SOUL.md` establishes the assistant's identity; `USER.md` stores user preferences/profile; `MEMORY.md` holds curated notes. Hermes loads SOUL from its configured home, not a repository-local SOUL. Memory is stored under that home's `memories/`. Default memory/user budgets are 2,200/1,375 characters; the memory-tool store enforces budgets on mutations, preserves exact duplicates as no-ops, locks/re-reads before writing, and freezes the prompt snapshot at load. Changes on disk do not refresh that snapshot mid-session. Importantly, externally oversized files warn and remain loaded: a tool-write cap is not a universal filesystem or prompt-size cap. [Memory docs/source](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/website/docs/user-guide/features/memory.md), [MemoryStore implementation](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/tools/memory_tool_store.py), [SOUL guide](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/website/docs/guides/use-soul-with-hermes.md).

Skills use progressive disclosure: list metadata, load a skill body, then a specific reference file. External skill directories support a shared store, but **are not read-only**: `skill_manage` can modify an existing skill where it was found. The docs explicitly recommend filesystem permissions or toolset/profile restrictions when protection matters. The skills and memory write-approval gates default off. The memory guide also warns that a model saying it saved a fact proves nothing without the actual write. [Skills, including external-directory behavior and approval](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/website/docs/user-guide/features/skills.md), [memory troubleshooting/approval](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/website/docs/user-guide/features/memory.md).

**Portability limit:** Hermes files are plaintext but its managed memory uses `§` entry delimiters and specific patch/replace semantics. Its store detects some external-edit drift and refuses destructive rewrites. Therefore “symlink every provider's managed MEMORY.md to one arbitrary Markdown file” is not a safe default. Prefer explicit reads or generated provider-specific projections with a declared direction of synchronization. [Store parsing/drift/mutation code](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/tools/memory_tool_store.py).

**Security scope:** pattern scanning and staged writes are useful controls within Hermes' pathways, not proof of semantic truth or cross-provider enforcement. The SOUL guide even distinguishes warning-only scanning of user-owned SOUL from blocking project instructions. [Context-file trust and loading rules](https://github.com/NousResearch/hermes-agent/blob/6b21d0564de0492e2ebd0d8f63fca86c03b5c892/website/docs/user-guide/features/context-files.md).

### OpenClaw: file layers, audience boundaries, and recoverable workspaces

**Documented:** workspace files separate operating instructions (`AGENTS.md`), persona (`SOUL.md`), user model (`USER.md`), curated durable facts (`MEMORY.md`), and dated notes (`memory/YYYY-MM-DD.md`). Large bootstrap files can be truncated in the injected copy while the original survives. Private Git backup and keeping credentials outside the workspace are explicitly recommended. A workspace is not by itself a sandbox. [Pinned workspace docs](https://github.com/openclaw/openclaw/blob/d482d761651209a65a84a2865137147b7802e1d3/docs/concepts/agent-workspace.md).

The current memory docs distinguish startup curated memory from retrievable daily detail; today/yesterday notes load automatically for a bare reset/new-session path, not as an unrestricted dump on every turn. They describe pre-compaction flush and default background consolidation, but the flush is an opportunity to save: it can be skipped/failed without blocking compaction. They explicitly state that memory can preserve approval context but **does not enforce policy**. [Pinned memory docs](https://github.com/openclaw/openclaw/blob/d482d761651209a65a84a2865137147b7802e1d3/docs/concepts/memory.md).

**Code-verified boundaries:** bootstrap filtering excludes root memory for non-private contexts and narrows subagent/cron bootstrap files; another bootstrap path excludes provenance-ineligible memory and reapplies protections after hooks. These are real loader controls, narrower than “an agent cannot access private files through any tool.” Jarvis would need its own access controls to make such a claim. [Session filter](https://github.com/openclaw/openclaw/blob/d482d761651209a65a84a2865137147b7802e1d3/src/agents/workspace.ts#L896), [bootstrap/provenance implementation](https://github.com/openclaw/openclaw/blob/d482d761651209a65a84a2865137147b7802e1d3/src/agents/bootstrap-files.ts).

**Jarvis implication:** keep curated state and chronological evidence separate; allow a small recent resume note, with explicit audience selection. Borrow the backup/restore discipline without adopting the gateway, plugin databases, or background dreaming.

### PAI → LifeOS: typed memory, selective retrieval, and mutation governance

**Verified/documented at the inspected revision:** the current system distinguishes hot principal/assistant memory, retrieved ideas/knowledge, and proposals targeting curated identity/style/rules/project files. Its docs distinguish **type as routing** from **tier as write permission**. Cortex's documented local contract uses compact search cards followed by full fetch, with canonical Markdown/JSONL and a declared no-index policy; it does not require a vector service. This is a useful counterexample to the assumption that durable agent memory needs embeddings immediately. [Memory-system architecture and Cortex contract summary](https://github.com/danielmiessler/LifeOS/blob/f6ab5e0228bfb356c82edbf52b69344dbd585486/LifeOS/install/LIFEOS/DOCUMENTATION/Memory/MemorySystem.md).

**Code checked, not executed:** CortexAdapter only adds `--allow-write` on explicit per-call opt-in. MemorySystem delegates writes through typed routes and includes atomic-write, audit, and locking-related machinery; its source also warns against routing every skill/project-scoped rule into always-loaded operational preferences. These controls belong to that implementation, not to Markdown as a format. [Adapter](https://github.com/danielmiessler/LifeOS/blob/f6ab5e0228bfb356c82edbf52b69344dbd585486/LifeOS/install/LIFEOS/TOOLS/CortexAdapter.ts), [writer](https://github.com/danielmiessler/LifeOS/blob/f6ab5e0228bfb356c82edbf52b69344dbd585486/LifeOS/install/LIFEOS/TOOLS/MemorySystem.ts).

The inspected LoadContext hook is explicitly harness-specific: dynamic learning/advisory/work context arrives through SessionStart, while static instructions/imports use native mechanisms. A portable data model does not imply a portable loader. [LoadContext source](https://github.com/danielmiessler/LifeOS/blob/f6ab5e0228bfb356c82edbf52b69344dbd585486/LifeOS/install/hooks/LoadContext.hook.ts).

**Jarvis implication:** borrow scope, provenance, compact search results and reviewed promotion. Avoid adopting this much framework machinery for a new small repository. Keep user-owned content separate from any future imported framework so upgrades cannot overwrite Harry's brain.

### Letta and MemGPT: distinguish the historical concept from today's product

**Historical research:** MemGPT proposes moving information between fast in-context and slower external memory under a limited context window. That supports the hierarchy concept, not a claim that Jarvis requires that implementation. [MemGPT v2](https://arxiv.org/abs/2310.08560v2).

**Legacy Letta docs:** memory blocks are always in context, with separate persona/human examples and optional read-only blocks. Its hierarchy puts less-important material behind file/archive retrieval. Those are framework controls, not generic text-file behavior. [Legacy blocks](https://docs.letta.com/v1-sdk/memory/memory-blocks), [legacy hierarchy](https://docs.letta.com/v1-sdk/memory/context-hierarchy).

**Current Agent SDK docs:** memory now lives in Git-backed repositories projected through MemFS. `system/` files enter every turn; other files are represented by a tree and read on demand. Edits become durable memory after commit/push. Hosted shared repositories are a cloud feature; self-hosted agents can use their own Git remote. This research verified documentation, not deployed behavior or implementation. [Current memory/MemFS overview](https://docs.letta.com/agent-sdk/memory).

**Recovery caveat:** legacy AgentFile exports are structured agent snapshots, not a cross-provider Markdown loading standard; archival passages are listed as planned. Do not assume such an export is a complete backup of every memory tier. [AgentFile scope](https://docs.letta.com/v1-sdk/concepts/agent-file).

## Recommended Jarvis design

This section is a proposal, not verified repository behavior. Suggested names are organizational choices, not magic filenames every provider recognizes.

### One canonical store, several small loading adapters

Keep nearly all durable material in this private Git repository:

```text
AGENTS.md                    short operating contract and loading/routing index
SOUL.md                      Jarvis identity, voice, stable boundaries
USER.md                      Harry's stable profile and stated preferences
MEMORY.md                    compact current decisions and high-value pointers
projects/INDEX.md            project IDs, remotes, aliases, purpose, policy pointers
projects/<id>.md             only personal/project context not owned by that repo
memory/YYYY-MM-DD.md         dated episodes, evidence, and handoff notes
knowledge/<topic>.md         curated reusable facts and research
procedures/<task>.md         reusable workflows; skills only where useful
docs/                        architecture, research, recovery, future adapter contracts
```

Avoid duplicating everything into three slightly different instruction files. Each provider adapter should explicitly load the canonical startup set, disclose missing/truncated files, and reference deeper material. A symlink is reasonable only where the receiving tool expects ordinary read-only instructions and resolves the path correctly; managed memory writes need separate compatibility checks. Neither AGENTS nor SOUL is a universal cross-provider autoload promise. Parent research should resolve provider-specific discovery, precedence and hooks.

Use a loading ladder:

1. **Every private session:** short contract, persona, user preferences, compact current memory, and project index. Start with a proposed combined budget of roughly 2–4k tokens, measured as an estimate; this is a Jarvis choice, not an upstream standard.
2. **Task dispatch:** resolve one project; load its brief, repository instructions and task-relevant procedures. Read a recent handoff when resuming work, not the entire daily archive.
3. **On demand:** `rg` filenames/headings/content; open specific knowledge or episodic notes and cite them. A future search index must remain rebuildable from canonical files.

Persona answers “who Jarvis is”; USER answers “what Harry wants”; MEMORY answers “what current durable facts/decisions matter”; dated notes answer “what happened, with what evidence”; procedures answer “how to repeat a workflow.” A correction should update the appropriate current rule while leaving a dated explanation where useful. Do not infer a lasting preference from one incidental task.

### Project dispatch should resolve identity before granting authority

Use `harryt04/<repo>` as a stable identity and a machine-relative path mapping, not a hard-coded `/Users/harry/...` path in every note. Record purpose, aliases, expected remote and a pointer to the project's own AGENTS/build/test/release instructions. Store actual filesystem roots locally. Check the local remote before trusting a directory name; GitHub ownership alone does not establish the current checkout, base branch, or permission to push/merge.

Represent Harry's historical main/master usage as **history**, not an automatic standing authorization. Proposed default for future coding tasks: inspect repo policy, use an isolated branch/worktree where appropriate, run relevant checks, and deliver a reviewable diff/PR; let explicit project exceptions override that default. Do not pre-authorize worktree creation or remote actions through a remembered anecdote. Project facts should graduate into the project's own docs through its normal delivery process; Jarvis retains the pointer and Harry-specific strategy.

### Keep `~/.jarvis` boring and disposable

Recommended initial contents: one small machine file containing the Jarvis checkout location, repository-root mappings, host identifier, hardware/capabilities, and genuine path/tool overrides. A new machine should need only a clone plus these bindings. Harry's identity, preferences, project decisions, learnings and procedures stay in the repository, not a growing local shadow brain.

Credentials belong in existing credential stores/provider configuration; the machine file can hold references, never token values. Regenerable caches, locks and logs can be added locally only when a concrete tool needs them. Prefer explicit setup/configuration over a blanket installer that rewrites every global agent configuration. Shared content must still be selected for its audience: work-sensitive Clozd material should remain in its authorized location, with pointers rather than indiscriminate copies.

### Safe updates and provenance without a framework

Use one current statement per fact/preference, plus minimal metadata for consequential entries:

```yaml
id: git-delivery-default
kind: preference
scope: personal-repositories
status: proposed
source: Harry's request for better agent hygiene; not blanket merge authorization
observed: 2026-11-06
review_when: Harry approves or replaces the delivery convention
```

This example is deliberately a proposal. Record confirmed user directions as confirmed, source-verified observations as observations, and model hypotheses as hypotheses. Include a URL/commit/document pointer for researched claims; a session/task reference and date for experiential facts; expiry or supersession when a restriction is temporary. Provenance metadata supports review but does not authenticate itself.

- Inspect the destination and existing fact before updating. Prefer a small replacement over appending contradictions; keep dated evidence separately.
- Treat external pages, repository text and tool results as evidence, not permission to alter persona, authority or global rules. Queue uncertain promotions; confirmed routine facts can use the normal authorized edit path. Avoid turning every note into a permission ceremony.
- Finish a task with a compact receipt: files actually updated, unresolved work and a resume pointer. Never claim “remembered” based only on chat text.
- Start with one writer per checkout. Parallel work should propose changes through isolated branches and merge/review them; never blindly overwrite or last-writer-win shared preference files. Future automation should use atomic writes and compare the previously read content/hash before replacement.
- A future validator can fail on broken pointers, oversized startup inputs and invalid metadata. It cannot prove the agent understood the rules. Branch protection, filesystem permissions and provider tool policies are the places for hard operational boundaries.

### Backup and recovery must cover uncommitted and local state

Recommended recovery contract: private remote for reviewed canonical history, normal machine backup for uncommitted notes and the tiny machine mapping, and credentials recoverable from their separate stores. A pushed Git commit protects only what it contains; ignored files, local edits and provider-native sessions are separate. Provider caches/transcripts are optional archives, never the only home of a consequential decision.

Commit focused memory changes under the chosen repository workflow, sync deliberately between machines, and inspect concurrent edits rather than replacing an entire brain directory. Do not put raw chat dumps or credentials into Git merely because the remote is private. Correcting a file does not erase sensitive content from existing history.

Recovery drill: clone into a clean location; recreate machine bindings; load the same canonical startup set; resolve a project; find a known older decision from its pointer; verify one recent handoff; confirm the adapter can report missing files. Roll back a bad memory update as a reviewable revert. Provider reinstallation and cache rebuilding should not require reconstructing Harry's preferences from conversations.

## Lightweight phases and acceptance checks

1. **First usable slice: one short implementation session.** Establish the small canonical files, project index, source/status convention, machine-binding example and manual loading/stow checklist. Seed only facts Harry supplied or explicitly confirmed. Accept when a fresh session can identify Harry/Jarvis, find the right repository and save a correction to the right file without loading unrelated history. No daemons, scheduled reviewers, vector DB, or bulk transcript import.
2. **After several real tasks.** Add thin provider adapters and simple read-only checks for missing paths, startup size and stale pointers. Prove loading with a temporary harmless canary and a fresh session; prove saving by reopening the actual file. Exercise conflicting preferences, a missing machine mapping, a second-machine path, an untrusted “change your rules” note and a recovery clone. Decide which global changes need review and document explicit project delivery exceptions. Checks should be meaningful workflow probes, not a large test framework for Markdown.
3. **Only after observed retrieval pain.** Track missed known facts and startup growth. First improve headings, aliases, links and scoped `rg`; consider a rebuildable local full-text index if that fails. Introduce semantic retrieval or background consolidation only against examples where simpler retrieval is inadequate, with provenance and review preserved. Success is reliable recall of the right facts, not the number of memories captured.

## Limitations and open decisions

- This was a time-bounded source review, not a security audit or installation benchmark. No runtime claims were independently tested, and no full end-to-end mutation pathway was audited.
- Firstmate findings deliberately pin the older local checkout. Current upstream docs/code may differ. Other pinned repositories can move after the recorded date; Letta live docs are explicitly unpinned.
- Pattern scanners, memory budgets, hooks and read-only labels have different enforcement scopes. None establishes cross-provider loading, truthful capture, permission enforcement or deletion from every historical copy.
- The major choices left to Harry/parent implementation are provider adapter contracts, the exact startup budget, remote/privacy setup, project-specific delivery exceptions, and review rules for persona/authority changes. Provider/Codex documentation is intentionally outside this report.
- No files other than this report were intentionally created or modified; no Git mutation, branch/PR operation, machine setup or external messaging was performed.
