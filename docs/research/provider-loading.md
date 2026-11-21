# Provider loading and portability

Inspected: 2026-11-06. These are documented behaviors, not results of testing installed harnesses.

Codex discovers global and project `AGENTS.md` guidance at startup. Its project walk follows the project root to the working directory; moving a shell into a sibling later is not a fresh startup. Jarvis must therefore explicitly load target guidance before editing. [Official OpenAI documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Claude Code's instruction-file support depends on version and settings. A `CLAUDE.md` containing `@AGENTS.md` is a documented compatibility bridge. Imports expand into startup context, so importing every project would defeat selective loading. Auto memory is a separate mechanism and should not become Jarvis's sole durable store. Verify actual loading in each supported client. [Official Claude Code memory documentation](https://code.claude.com/docs/en/memory).

Implemented 2026-11-10 at Harry's request: Jarvis bridges Claude Code with symlinks rather than an `@AGENTS.md` import file. `CLAUDE.md -> AGENTS.md` keeps one canonical instruction file, and `.claude/skills -> ../skills` exposes the Jarvis-owned skills as Claude Code project skills. Symlinks require a filesystem and Git checkout that preserve them (`core.symlinks`); on Windows without symlink support, fall back to a `CLAUDE.md` containing `@AGENTS.md`. Verified only that the links resolve in a Linux checkout; Claude Code's loading of them takes effect at the next session start in the checkout.

Observed 2026-11-21 (Antigravity built-in customization guide and live T3 Antigravity session): Google Antigravity natively discovers `AGENTS.md` (alongside `GEMINI.md`) and `.agents/skills/*/SKILL.md` by walking up from the working directory to the repository root; it does not scan `.claude/skills/`. Rule files are capped at 24 KB (`24,000` bytes) each and share a `20,000`-token aggregate budget, so keeping `AGENTS.md` concise and placing procedures in `.agents/skills/` preserves progressive disclosure. Do not add a duplicate `GEMINI.md` alongside `AGENTS.md`. Machine-local global skills live under `~/.gemini/config/skills/` (distinct from `~/.agents/skills/` and `~/.claude/skills/`). Jarvis exposes all Jarvis-owned skills in `.agents/skills/` via relative symlinks to `../../skills/<name>` so Antigravity and Codex discover the same set as Claude Code.

## Proposed adapter contract

Canonical content stays in ordinary Markdown and a small project registry. Each adapter only ensures that the session reads the shared startup contract and can locate the checkout. Tool permissions, sandbox access to siblings, installed skill discovery, and event-driven task supervision are harness concerns. A text file does not supply those capabilities.

For another provider or a chat without local filesystem access, supply a deliberate context bundle or authorized read-only retrieval connector. Only the included/retrieved material is available there. Writing a memory back requires an explicit supported path; do not promise automatic sync to arbitrary chats.

Test launch adapters with a fixed question set and inspect their loaded instructions or logs. A fluent claim that the assistant is Jarvis is weaker evidence than identifying the correct files, project exception, and next reading step.
