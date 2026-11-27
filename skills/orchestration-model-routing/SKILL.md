---
name: "orchestration-model-routing"
description: "Use before spawning, delegating to or briefing a subagent, worker or child thread, and when choosing or comparing models, providers or effort levels for delegated work. Reads what this session can spawn, each provider's quota and slopalytics.com benchmarks, then confirms the spawn plan with the developer."
---

# Orchestration model routing

An orchestrator spends the developer's usage on other models. Route from **evidence read now**: the
models this session can start, the quota each provider has left, and current benchmark numbers.
Model names, prices and limits change within weeks, so a pick made from what you remember is a guess.

The result of this skill is a **spawn plan**: one line per worker with its provider, model and
effort, the evidence for the pick and the quota behind it. The developer sees the plan before the
first worker starts.

Commands run from the root of the Jarvis checkout. In a repository this skill was copied into,
run them from that repository's root.

## 1. Read what the developer fixed

Collect every limit the developer gave: models, families, effort ceilings, agent count, budget,
deadline. Routing happens inside these limits. A limit that can be read two ways is a question for
step 7: "Opus 5.5 medium or below" may or may not allow a smaller Claude model.

When the developer asks for a [council](../council/SKILL.md), its shape is a limit: three
workers, one flagship model from each of three providers, at high effort, read-only for review.
Council picks the providers; this skill still reads capability, quota and benchmarks and shows the
plan for a yes in step 7. Harry's instruction, 2026-11-27.

Done when each limit is written down, or you can say "none stated".

## 2. Decide whether to spawn

A worker starts with none of your context and hands back a summary. Do the work yourself when it
is a handful of tool calls or a lookup whose target you know. Spawn for independent work that can
run in parallel, for a check by a model from another family, or to keep long output out of your
context. Plan the fewest workers that cover the independent parts.

## 3. Read what this session can spawn

In T3 Code, call `orchestrator_capabilities`: once per thread, and again after a spawn error or when
the developer names a provider it did not list. For each provider read whether it can run a child
task, its model ids, and the name and allowed values of its effort option. Claude, Codex and
Antigravity each name that option differently, and each model has its own default.

In another harness, read that harness's own model list.

A provider that is disabled or absent cannot be used. Say so in the plan and offer the nearest
available pick. Substituting quietly spends usage the developer never agreed to.

Done when you hold the list of provider, model and effort values this session can start.

## 4. Read quota

Run `npx -y quota-axi`. Its `--help` owns the field meanings. Add
`--full` only when you need pace or the projected exhaustion time; that output also holds account
identity, which stays out of worker briefs and external requests.

quota-axi names providers `claude`, `codex` and `agy`. T3 Code names the same three `claudeAgent`,
`codex` and `antigravity`. Your own session spends its provider too while it plans and reviews.

quota-axi reports and never recommends. Put each provider you might spend in one state:

| State | Read it from | What it allows |
| --- | --- | --- |
| **clear** | The runway lasts through the reset, and the planned work is small beside what is left | Spend it |
| **tight** | Projected to run out before the reset, ahead of pace, or under 20% left | Spend only on the developer's yes; show the nearest pick from a clear provider |
| **unknown** | Listed under `attention`, or missing | Give the developer its `remedy` line. Unknown is not headroom: spend only on their yes |
| **exhausted** | Listed under `exhaustion` | Do not plan work on it |

On a long run, read quota again before each new batch of workers.

Done when each provider in the plan has one line: percent left, reset time and state.

## 5. Read the benchmarks

slopalytics.com is this skill's benchmark source for comparing models. It republishes Artificial Analysis data for each model at each effort level: an
intelligence index, a coding index, cost per task and seconds per task. The page loads its data
with JavaScript, so read it with the bundled script:

```sh
node .agents/skills/orchestration-model-routing/scripts/slopalytics.mjs \
  --models claude-opus-5-5,gpt-6.2-sol,gemini-4-neon --effort low,medium
```

Pass the model ids from step 3 and every effort level you may run. `--help` lists the other flags.

- A model the script reports as not on the site is **unbenchmarked**. Say so; do not estimate it.
- The site does not measure hallucination rate, long-context recall, web research or writing
  quality. For those, use vendor guidance and say the claim is not benchmarked.
- When the script fails, use [references/benchmark-snapshot.md](references/benchmark-snapshot.md)
  and tell the developer its date.

Done when every candidate has numbers at the effort you would run it at, or is marked unbenchmarked.

## 6. Choose

For each worker, in this order:

1. Stay inside the developer's limits and the list from step 3.
2. Compare at the effort you will run. A score at max says nothing about medium, and effort moves
   scores more than family does.
3. Read the index that matches the work: coding for code, intelligence for reasoning, research,
   synthesis and planning.
4. Among models with close scores, take the lower cost per task, then the fewer seconds per task.
   A model that takes many minutes per task suits an unattended run, not a developer who is waiting.
5. For bulk search, extraction and classification, take the cheapest model that is good enough.
6. Leave out a provider that is tight or unknown unless the developer says yes.
7. Give a review or a fact-check to a family other than the one that wrote the work.

## 7. Show the spawn plan and confirm

Show the plan before the first spawn, every time:

```text
Spawn plan
| # | Task | Provider · model · effort | Evidence at that effort | Quota |
| 1 | <task> | <provider> · <model> · <effort> | intelligence <n>, coding <n>, $<n> and <n>s per task | <provider>: <n>% left, resets <local time>, <state> |
Limits you set: <each limit, or none>
Benchmarks:     slopalytics.com, site snapshot <date> | dated snapshot file <date>
Not benchmarked: <each claim or model with no number behind it, or none>
Your session:   <provider and model that plans and reviews>
Question:       <the one thing in doubt, with your recommendation> | none
```

**When in doubt, ask and wait for the answer.** Any one of these is doubt:

- The developer named no model or no effort, or a limit can be read two ways.
- A model or provider they named is unavailable, or the plan substitutes anything.
- A provider in the plan is tight or unknown.
- The plan spends a provider the developer did not mention.
- The plan has more than four workers, an effort above high, or a pick that costs several times
  the next best per task.
- The benchmark read failed, or a pick is unbenchmarked.
- Two picks are too close to call for the work that decides the result.

Ask one question, recommendation first, with the choices. With no doubt (the developer fixed the
model, effort and worker count, all are available and quota is clear), show the plan and start in
the same turn.

One yes covers that plan. Ask again before you add a provider, raise a model or effort, or add
workers. With no human present, start only what the developer's standing instructions already
cover, and report the open question.

## 8. Spawn and brief

- Set the model and the effort option on every spawn. Do not rely on a default.
- Brief each worker with the guard for its family from
  [references/briefing-traps.md](references/briefing-traps.md).
- Read the executed model from the spawn result. When it differs from the plan, tell the developer.

## 9. Report

In the final reply, name each worker's model and effort, any pick the developer changed, and each
claim that stayed unbenchmarked.

## Keeping the research current

The two reference pages are dated. When a date is more than 14 days old, or the session's model
list names a model they do not mention, tell the developer and offer
[references/refresh-model-research.md](references/refresh-model-research.md).
