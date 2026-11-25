# Briefing traps by model family

Read the lines for a worker's family before you write its brief, and put the matching guard in the
brief. Vendor-stated in each family's prompting guide, read 2026-11-24, unless marked observed.

Tell every research worker that its training data predates today's products, and that each claim
needs a page it opened in this session.

## Claude

- Opus 5.5 can end a long task with a text-only summary, which stops an unattended loop. Give it a
  checklist. Its default effort is medium.
- Sonnet 5.5 at low reports done without running checks, and adds tests and docs nobody asked for.
  State the done criteria and the scope.
- Haiku 5.5 at low skips searches and checks in long prompts. Use medium.
- Sonnet 5.5 and Haiku 5.5 answer from training data when a search would catch a changed fact. Tell
  them to search.
- Fable 5.2 ends turns early at low and medium, and reads "never" as absolute. Add "finish the
  whole task".

## OpenAI (Codex CLI)

- Web search is cached by default. Live search needs `--search` or the full-access sandbox, so say
  "live web search" in a research brief.
- The `ultra` effort lets the model spawn its own subagents. Leave it to a worker whose parent does
  not delegate.
- Keep briefs lean: authorized actions, completion checks, how to report a blocker. GPT-6 Astra may
  pause for clarification or run broader tests than asked.
- Naming: Astra is the frontier tier, Sol the workhorse, Terra the visual, computer-use and writing
  model, Luna the cheap tier.

## Gemini (Antigravity)

- Naming: Carbon is the deepest tier, Neon the balanced one, Hydrogen the fast executor. An
  Orchestrator model plans with Carbon, Neon or Argon and executes with Hydrogen; its effort is fixed.
- A subagent starts with no parent history. Give it the verification commands.
- In the Gemini API, Google Search grounding and URL context are opt-in tools. Whether Antigravity
  sessions get web search by default was not found in Google's docs.
- No Gemini 4 model accepts the `minimal` thinking level.
- Observed in one research session: Gemini 4 Neon at medium took the longest of the three families
  on the same brief.

## T3 Code delegation (observed 2026-11-24)

- Provider ids are `claudeAgent`, `codex` and `antigravity`. The effort option is `effort` for
  Claude, `reasoningEffort` for Codex and `thought_level` for Gemini. `orchestrator_capabilities`
  is the live source; these names are here so a mismatch is easy to spot.

## Sources read on 2026-11-24

- Anthropic: the model overview, effort and release-notes pages, and the prompting guides for
  Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5, all under `platform.claude.com/docs`.
- OpenAI: the Codex model guide and prompting guide under `learn.chatgpt.com`, and the API model
  pages and changelog under `developers.openai.com/api/docs`.
- Google: the model, thinking, pricing and deprecation pages under `aistudio.google.com/docs`, and
  the model and subagent pages under `antigravity.google/docs`.

To refresh this page, follow [refresh-model-research.md](refresh-model-research.md).
