---
name: t3-session-spawner
description: Launch separate top-level T3 sessions in Jarvis for sibling repositories, optionally distributing them across linked machines. Use for /t3-session-spawner, starting T3 sessions or threads on Harry's behalf, or preparing their launch prompts. Distinguish these sessions from delegated subagents; prompt preparation alone does not launch work.
---

# T3 session spawner

T3 can expose `t3_thread_launch` to create independent, top-level sessions on
Harry's behalf. These are visible T3 threads, distinct from native subagents
and `delegate_task` children. Do not infer that session launching is impossible
because a tool is absent from the initial tool list or another agent said so.
Availability depends on the current harness and connected environments.

Use this capability when Harry requests new sessions/threads, or an invoked
workflow explicitly calls for them. A request for subagents does not mean new
top-level threads. A request only to prepare prompts does not authorize launching.
Creating or updating this skill does not itself launch anything. Preserve the
work's existing merge/deploy authority; spawning grants neither.

## Confirm the batch before launching

Before the first launch, remind Harry that a descriptive orchestration-thread
name makes worker links easier to find. Suggest renaming it before spawning.
Offer to pin the orchestration thread and keep it active, or ask whether he
wants it to auto-settle after all approved sessions have been dispatched.
Bundle this with the model/batch question where practical. Honor an existing
explicit answer rather than asking repeatedly. Do not rename, pin, unpin or
settle merely because those tools exist. Use `t3_thread_update` for an agreed
name and `t3_thread_organize` for an agreed pin/settle choice; if unavailable,
give the user the corresponding UI action. Do not promise pinning prevents
all automatic settling. Avoid linking worker PRs to the coordinator just for
tracking: linked PR merges can settle a thread. Keep receipts in ~/.dexter.

Confirm **provider, model and reasoning effort** for this batch before any
session starts. Present the workflow/default selection as a recommendation,
not confirmation. An explicit choice already given for this batch satisfies
the question; a saved preference or inherited model alone does not. If Harry
wants the current selection, read it with `t3_thread_configure` (or the current
capability response) and name the actual values for confirmation. For example:
"Use GPT-6.1 Sol with medium reasoning for these five sessions? Keep this
orchestration thread pinned and active, or settle it after dispatch?"

T3 supports `modelSelection` on `t3_thread_launch`; use it to apply the
confirmed provider/model/options without manual UI setup. Inspect live schema
and provider catalog for option names. If the harness only supports inherited
settings, tell Harry to select that provider/model/effort in the orchestration
thread's model controls before launching, then reread and verify the selection.
If the requested model is unavailable, report that and leave affected targets
unlaunched until he selects an available model; never silently substitute.

Confirm the approved target set, concurrency limits and whether automatic
queue refill is wanted. "First five; wait for my green light" approves only
those five, regardless of idle capacity. Do not create scheduled work from a
request to discuss or document queueing. Naming/pinning is optional; model and
scope confirmation are required before dependent launches.

## Discover tools before claiming a limitation

Follow Jarvis's safe `origin/main` refresh and context loading first. Discover
T3 tools using the current harness's tool search; in Codex code mode, search
`ALL_TOOLS` by name/description and call discovered methods through `tools`.
Other harnesses may provide ToolSearch. Do not require a tool literally named
ToolSearch when another discovery mechanism exists.

Look for `t3_thread_launch`, `t3_project_list`, `t3_thread_read`, and, for remote
machines, `t3_environment_links` / `t3_environment_link`. Inspect the callable
schema rather than guessing provider/model fields. Deferred tools can load late;
try the named tool once before declaring it unavailable. Never make a test
launch just to probe capabilities when launching has not been requested.

Report limitations narrowly: e.g. "local session launch is available; linked
machine discovery is unavailable here." A missing remote tool does not imply
local launching is impossible. If launching fails or remains unavailable,
report the actual error/missing tool and provide copy-paste prompts for the
affected targets; do not silently substitute subagents, CLI agents, or a
Workflow. Do not assume documentation proves a launch succeeded.

## Select Jarvis projects and machines

- Resolve each target through `projects/catalog.json` and its brief. Exclude
  retired identities; aliases and folder names are not repository identities.
- List current-environment projects with `t3_project_list`, following pagination.
  Select the active project whose repository identity is
  `github.com/harryt04/jarvis`, not just one titled "Jarvis". Project IDs and
  filesystem paths are machine-specific; discover them afresh.
- For distribution, use `t3_environment_links`, then list projects on each
  answering environment with its `environmentId`. Keep machines with Jarvis.
  Prefer those with the intended target checkout as Jarvis's sibling.
  Registrations are discovery evidence; workers must verify actual origins.
- If Harry names an unlinked machine, use `t3_environment_link` with a `hint`
  from his words. Do not ask for pairing codes in chat. Follow the tool's
  secure connection flow. If unavailable, report that specific blocker.
- Balance eligible assignments by active workload when available, otherwise
  round-robin by assigned count and disclose that this is count balancing,
  not measured CPU capacity. Respect requested batch/resource limits. Avoid
  duplicate sessions by checking existing work and retaining launch receipts.
  A missing sibling is a blocker, not permission to clone or use another repo.

## Launch in Jarvis

Use `t3_thread_launch` once per target. Pass the chosen environment's **Jarvis**
`projectId` and its `environmentId` (omit environmentId for local calls).
Set `workspaceStrategy: {type: "root"}` explicitly: this binds the session to
the Jarvis primary checkout, even when the caller is in a task worktree.
Do not bind it to the target project, scratch, or a new Jarvis worktree.
The worker locates `../<catalog-folder>` from primary Jarvis and acquires the
**target repository's** Treehouse worktree for edits.

Pass a descriptive `title`, the entire self-contained worker prompt as
`message`, and a stable `clientRequestId` such as `<task>-<repo>-<run-id>`.
Reuse that ID after an error/lost reply to avoid duplicate threads. Distinct
intentional reruns need distinct run IDs. Retain the receipt before retrying.
Inherit runtime modes; do not elevate them. Use the batch-confirmed
provider/model/effort, using the current schema/catalog to construct
`modelSelection`. Inherit the current model only when Harry confirmed that
selection for this batch. Do not substitute an
unavailable requested model unasked. `orchestrator_capabilities` can help
resolve available providers/models; its child-agent feature flags alone do not
prove `t3_thread_launch` availability.

Minimal shape (fill values from live discovery, not this example):

```json
{
  "projectId": "<Jarvis project on the selected machine>",
  "workspaceStrategy": {"type": "root"},
  "title": "<task>: <target>",
  "message": "<complete worker task>",
  "clientRequestId": "<task>-<target>-<unique run id>"
}
```

The worker prompt must carry enough context for a fresh session: safely refresh
Jarvis origin/main and reread context; verify the sibling origin and current
instructions; fetch the target's actual default branch (often master); use a
Treehouse task worktree; perform the scoped task and checks; deliver the
specified PR/results contract; report missing access and limits. A pointer to a
local file is insufficient on another machine. Do not assume another session
inherits this chat, unmerged Jarvis changes, or this machine's `~/.dexter`.

## Concurrency and queue refill

For an approved queue, read [queue coordination](references/queue-coordination.md).
It explains configured slots versus hardware telemetry, durable local queue
state, and T3 scheduled coordinator turns. A skill document alone is not a
running dispatcher. Do not promise automatic refill without a supported wakeup
mechanism and an enabled, authorized coordinator task. Pinning a thread does
not keep the agent executing after a turn ends.

## Report, fallback and storage

Follow the launch tool's required `t3_thread_read` or `t3_thread_wait` follow-up,
and any returned `next` instruction. Do not poll workers until completion just
to confirm creation. Use a short initial read where supported. Report target,
environment, actual launch state, and the returned thread `link` verbatim.
Read a thread before answering questions about its progress. Distinguish a
created/queued thread from a successful completed task. For partial failures,
keep successful receipts and retry/fallback only failed targets.

When printing prompts, output one complete fenced Markdown block per target,
state the model and Jarvis starting project, and list exclusions with reasons.
Self-contained Markdown can be copied into fresh sessions without inherited
history. Save ad hoc plans, rendered prompt packs, assignments and receipts
under `~/.dexter/tasks/<task>/`, outside Git. Reusable skill instructions belong
in Jarvis; creating a one-off plan does not require a Jarvis PR. Preserve any
explicit workflow-specific durable run-log contract, such as Lighthouse's
minimal dates/repos log; do not add prompts or machine state to it.

Verification, 2026-11-10: five Node 26 sessions were created in the local Jarvis
project with GPT-6.1 Sol / medium; initial reads confirmed preparing/starting.
This validates local dispatch, not completed migrations. Linked-environment
discovery was unavailable. Environment read exposed platform/preferences, not
CPU/RAM utilization. Scheduled queue refill, thread lifecycle preferences and
cross-machine launching have not been exercised by this skill. Discover live
capabilities before making claims about them.
