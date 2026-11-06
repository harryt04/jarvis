# Provider loading and portability

Inspected: 2026-11-06. These are documented behaviors, not results of testing installed harnesses.

Codex discovers global and project `AGENTS.md` guidance at startup. Its project walk follows the project root to the working directory; moving a shell into a sibling later is not a fresh startup. Jarvis must therefore explicitly load target guidance before editing. [Official OpenAI documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Claude Code's instruction-file support depends on version and settings. A `CLAUDE.md` containing `@AGENTS.md` is a documented compatibility bridge. Imports expand into startup context, so importing every project would defeat selective loading. Auto memory is a separate mechanism and should not become Jarvis's sole durable store. Verify actual loading in each supported client. [Official Claude Code memory documentation](https://code.claude.com/docs/en/memory).

## Proposed adapter contract

Canonical content stays in ordinary Markdown and a small project registry. Each adapter only ensures that the session reads the shared startup contract and can locate the checkout. Tool permissions, sandbox access to siblings, installed skill discovery, and event-driven task supervision are harness concerns. A text file does not supply those capabilities.

For another provider or a chat without local filesystem access, supply a deliberate context bundle or authorized read-only retrieval connector. Only the included/retrieved material is available there. Writing a memory back requires an explicit supported path; do not promise automatic sync to arbitrary chats.

Test launch adapters with a fixed question set and inspect their loaded instructions or logs. A fluent claim that the assistant is Jarvis is weaker evidence than identifying the correct files, project exception, and next reading step.
