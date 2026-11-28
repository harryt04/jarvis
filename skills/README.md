# Skill catalog

This catalog covers every skill currently stored in `skills/`. The skill files
remain the source of truth for full instructions and invocation details.

| Skill | What it does |
| --- | --- |
| [agent-browser](agent-browser/SKILL.md) | Uses the `agent-browser` CLI to navigate and inspect web pages, interact with forms, and capture screenshots or audits. |
| [app-design](app-design/SKILL.md) | Turns a new app idea into an approved visual design and build plan before implementation. |
| [catalog](catalog/SKILL.md) | Prints this catalog as a Markdown table in chat when invoked with `/catalog`. |
| [chief-of-staff](chief-of-staff/SKILL.md) | Coordinates a long-running goal across subagents and schedules in one session. |
| [code-review](code-review/SKILL.md) | Reviews a change against repository standards and its originating specification. |
| [code-with-restraint](code-with-restraint/SKILL.md) | Guides production implementation and refactoring toward clear, evidence-backed designs. |
| [council](council/SKILL.md) | Calls a multi-provider group of delegates to review or advise on a request. |
| [dependabot-cleanup](dependabot-cleanup/SKILL.md) | Resolves and merges eligible Dependabot PRs across Harry’s repositories, subject to its scoped rules. |
| [find-issues](find-issues/SKILL.md) | Finds and verifies unreported bugs or performance improvements without filing issues or PRs. |
| [find-issues-make-pr](find-issues-make-pr/SKILL.md) | Finds, verifies, fixes, and publishes repository issues and PRs when explicitly requested. |
| [gh-axi](gh-axi/SKILL.md) | Operates GitHub through the `gh-axi` CLI, including issues, PRs, CI, releases, and Projects. |
| [grill-me](grill-me/SKILL.md) | Interviews the user to sharpen a plan or design through focused questions. |
| [grill-with-docs](grill-with-docs/SKILL.md) | Sharpens a plan through an interview while creating supporting ADR and glossary documents. |
| [handoff](handoff/SKILL.md) | Produces a compact handoff document so another agent can continue the current work. |
| [implement-spec](implement-spec/SKILL.md) | Implements the result of the `/to-spec` and `/to-tickets` workflows. |
| [lavish](lavish/SKILL.md) | Creates rich HTML artifacts that users can review and annotate. |
| [lighthouse-audit](lighthouse-audit/SKILL.md) | Runs and coordinates Lighthouse audits across cataloged web repositories and prepares fixes as PRs. |
| [machine-init](machine-init/SKILL.md) | Sets up indexed repositories, shell aliases, and available coding-agent sign-ins on a local or remote machine. |
| [omarchy-steam-setup](omarchy-steam-setup/SKILL.md) | Installs Steam on an Omarchy machine and gets it to the sign-in window, using muvm and FEX on Apple Silicon. |
| [orchestration-model-routing](orchestration-model-routing/SKILL.md) | Checks delegation options, quotas, and model benchmarks before briefing workers or selecting models. |
| [pr](pr/SKILL.md) | Guides writing a clear pull-request body. |
| [security-review](security-review/SKILL.md) | Reviews cataloged repositories for application security issues and handles scoped Dependabot remediation. |
| [show-me](show-me/SKILL.md) | Explains a topic visually with concise diagrams, code sketches, or focused HTML. |
| [skill-copy](skill-copy/SKILL.md) | Copies selected Jarvis skills into sibling repositories for Claude Code, Codex, and Antigravity. |
| [software-factory](software-factory/SKILL.md) | Provides shared terminology for designing a software factory and its tasks, triggers, runs, and services. |
| [t3-session-spawner](t3-session-spawner/SKILL.md) | Launches separate top-level T3 sessions or prepares prompts for sibling repositories. |
| [teach](teach/SKILL.md) | Teaches a topic over multiple sessions using lessons and learning records in the current workspace. |
| [to-questionnaire](to-questionnaire/SKILL.md) | Creates a questionnaire to collect decisions or facts from someone with relevant expertise. |
| [to-spec](to-spec/SKILL.md) | Synthesizes the current discussion into a specification and publishes it to the configured issue tracker. |
| [to-tickets](to-tickets/SKILL.md) | Breaks a plan or spec into dependent tracer-bullet tickets and publishes them to the configured tracker. |
| [treehouse-cleanup](treehouse-cleanup/SKILL.md) | Reclaims only verified-clean Treehouse slots whose PRs have merged, stopping processes inside those slots. |
| [unslop](unslop/SKILL.md) | Edits writing to remove common AI-generated patterns while preserving meaning and tone. |
| [wait-what](wait-what/SKILL.md) | Re-explains a message in plain, simplified technical English when the prior explanation did not land. |
| [writing-for-agents](writing-for-agents/SKILL.md) | Guides writing skills and other documentation that agents use as instructions. |
