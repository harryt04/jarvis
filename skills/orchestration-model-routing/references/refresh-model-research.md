# Refresh the model research

This skill's two reference pages are a cache of the outside world:
[briefing-traps.md](briefing-traps.md) (how each family behaves as a worker) and
[benchmark-snapshot.md](benchmark-snapshot.md) (the dated fallback table). New models ship within
weeks, so the cache goes stale.

Refresh when any of these is true:

- A date in either page is more than 14 days old.
- The session's model list (SKILL.md step 3) names a model that neither page mentions.
- The developer asks for current model research.

Otherwise report the two dates and stop.

## Steps

1. **Route the research with this skill.** The refresh is delegated work: run SKILL.md steps 1 to 7
   for it and show the spawn plan. In a routine with no developer present, use the cheapest clear
   provider that meets the brief and report what you chose.
2. **Benchmarks, no worker needed.** Run
   `node .agents/skills/orchestration-model-routing/scripts/slopalytics.mjs --effort medium,high`
   and rewrite `benchmark-snapshot.md` from its output: the site's snapshot date, the medium table,
   and what the numbers say about the default worker, the hardest work, cheap bulk work and any
   model too slow to wait on. Label that reading as inference.
3. **Vendor research, one worker per family** in the session's model list (Anthropic, OpenAI,
   Google today). Each worker reads that vendor's own current docs on the live web and reports:
   - the models available now, with release dates and any announced removal;
   - what the vendor says each model and each effort level is for, and the default effort;
   - prompting guidance that matters when the model is briefed as a worker;
   - limits that change a brief, such as whether a session has live web search.
4. **Independent standing, one worker.** It reads third-party evidence on how the families compare
   for research, long documents, coding, review and bulk work, and says where that evidence is
   thin, vendor-run or missing. slopalytics.com stays the source of truth for scores; this worker
   covers what the site does not measure.
5. **Cross-check.** A worker from a different family than the author checks every claim that would
   change a line in `briefing-traps.md` or a routing rule. A claim counts as confirmed only when a
   primary source opened in that session says so.
6. **Write.** Update `briefing-traps.md` with the new date, lines and sources. Mark each line
   vendor-stated, third-party or observed. Remove a line whose model is gone.

## Put this in every research brief

- You are a research worker, not the orchestrator. Do only this task. Read-only: change no file and post
  nowhere.
- Today's date. Your training data predates these models, so answer from pages you open in this
  session, and give the URL for each claim.
- Label each claim vendor-stated, third-party or your inference. Say plainly what you could not
  find or verify, and say so if you had no web access.
- Put no company name or internal detail into a web search.
- A word limit and the output shape: one table, then routing rules, then sources.

Done when both pages carry today's date or a stated reason they did not change, and every changed
line has a source a reviewer can open.
