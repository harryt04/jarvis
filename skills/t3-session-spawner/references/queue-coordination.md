# Queue coordination

Read when Harry wants the spawner to maintain concurrency and dispatch more
approved targets as slots free. This is a procedure using T3 tools, not an
installed service or a claim that one is already running.

## Capacity evidence

`t3_thread_list` exposes statuses, not hardware headroom. List all relevant
projects and pages on each reachable environment to account for other work;
read tracked worker threads to distinguish a finished turn from a finished
task. `t3_environment_read` currently exposes platform/preferences, not CPU
load, available memory, disk pressure or provider quota. `t3_queue` manages
messages queued to one thread, not a fleet-wide job scheduler.

Use confirmed global and per-environment session limits. Within the approved
set, place work on an eligible machine with the fewest reserved slots. Call
this slot/count balancing, not resource-aware scheduling. Heavy-command locks
can additionally cap builds on one machine; they do not coordinate other
machines or measure resource usage. Do not infer free RAM from idle threads.

Local shell access can inspect local CPU/memory/disk without a T3 telemetry
API, but is not remote telemetry. Cross-machine hardware-aware placement
requires a discovered supported telemetry tool or a separately implemented
and authorized remote probe. If unavailable, report the limit and use configured
caps. An unreachable environment is unavailable capacity, not an idle machine.

## Durable queue and dispatch pass

Keep state under `~/.dexter/tasks/<task>/` on the coordinator machine: approved
IDs, deferred/unapproved IDs, confirmed model/options, session and build caps,
project/environment IDs, per-target state, reserved slots, stable launch IDs,
thread links, latest evidence, coordinator scheduled-task ID and settle choice.
Pass full prompts to remote launches; never rely on their reading this path.

Each coordinator pass must:

1. Acquire an exclusive local dispatcher lock. If another pass owns it, exit
   without dispatching. Use atomic state-file replacement. Run a single
   coordinator owner; a local lock does not protect multiple-machine writers.
2. Reconcile launch receipts against live thread state and current environment
   access. Reserve slots before launching and persist each receipt. Unknown
   launch outcomes retain the reservation until reconciled or retried with the
   same clientRequestId; never compensate with a second new launch ID.
3. Count preparing/queued/starting/running workers as reserved. Waiting or idle
   workers may resume, and a completed agent turn can still have pending work;
   do not release their reservations merely from a status string. Read their
   latest evidence. Release a slot when the worker has delivered the agreed
   final result, or failed/cancelled with no live work. PR review handoff can be
   a completed worker task when its contract is review-only. Leave blocked work
   visible and record whether it is stopped or can resume before reusing slots.
4. Dispatch only enough approved pending targets to fill confirmed global and
   per-machine slots; never automatically expand the approved set. Use the
   confirmed model, Jarvis-root launch and initial-read contract from SKILL.md.
   Unsupported models, missing checkouts and offline machines remain blocked.
5. Persist progress and exit. Do not keep the agent alive with sleep loops or
   repeatedly poll workers in one turn. Reconcile on the next authorized
   scheduled turn or supported event. PR waits use watch_pull_request, not a
   separate queue-monitor workaround.

## Continue after the turn ends

T3 exposes `schedule_task` for persistent scheduled turns. With Harry's request
for automatic queue refill, configure one bounded coordinator task bound to the
orchestration thread (`bindToCurrentThread: true`); choose a modest agreed
cadence, e.g. five minutes, rather than busy polling. Include the absolute
state path, approved scope, model/options, limits, lock/reconciliation rules,
stopping conditions and no-merge/deploy boundary in its prompt. Scheduled runs
may start without earlier context, so the prompt/state must be sufficient.
Inspect the live schema; interval minimum is currently one minute. Report the
returned task ID, enabled state, policy blocker if any and next run time. A
blocked/disabled schedule is not an active dispatcher. If scheduling is absent,
report that refill needs another user turn; do not claim passive monitoring.

While the queue is active, retain the coordinator thread for scheduled work and
report completion separately from dispatch. If Harry chose auto-settle after
all approved sessions are dispatched, disable the dispatch schedule once there
are no approved pending/uncertain launches, save receipts, then settle at turn
end. If he asked to monitor workers through completion, wait for that contract
instead. Never auto-settle with blocked undispatched targets or silently
abandon a queue. Pause/disable the coordinator when all remaining work needs
user input; resume only after that input. No recurring task should keep firing
forever on an empty or blocked queue. Do not install a scheduler just to test
this procedure.
