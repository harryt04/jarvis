# Jarvis

Harry Thomas's portable context for AI work: identity, working preferences, project knowledge, decisions, and lessons that should survive a new chat, model, provider, or machine.

**Status: research, setup plan, and initial knowledge seed.** Harry authorized publishing this foundation to the private repository's default branch, `main`. The retained project briefs are source snapshots; implementation proposals remain labeled. No startup adapter, installer, background agent service, or shared-memory synchronization has been installed. Machine-local research coordination state lives outside this repository.

Start with [the setup plan](docs/setup-plan.md). The recommendation is a small, Git-backed knowledge workspace, with provider-specific entry points and project context loaded when needed. Firstmate is a useful orchestration reference; Jarvis does not need a fleet supervisor to begin remembering.

The [rollout map](docs/jarvis-map.html) provides an interactive overview of the proposed storage boundaries and phases.

## Initial knowledge

- [Harry](context/harry.md): confirmed context, historically recorded preferences, and unknowns.
- [Jarvis](context/jarvis.md): proposed persona and communication contract.
- [Working agreements](context/working-agreements.md): observed workflow policy and proposed improvements.
- [Projects](projects/README.md): current routing and availability, with confirmed deletions excluded.
- [Project registry](projects/catalog.json): identities, aliases, discovery evidence, and reading entry points.
- [Source learning pass](projects/briefs/README.md): retained source briefs, with evidence, task-reading maps, and explicit verification limits.
- [Portfolio findings](docs/research/portfolio-findings.md): cross-project lessons and separately scoped follow-up candidates.
- [Discovery evidence](docs/research/local-discovery.md): scope, mismatches, and limits.
- [Coolify recovery](docs/research/coolify-deployment-recovery-2026-11-07.md): deployment audit, verified recovery results, and Caddy analytics requirements.
- [Coolify MCP](docs/integrations/coolify-mcp.md): endpoint, token location (`~/.jarvis/secrets/`), agent quick start, authority boundary, and production inventory.
- [Provider loading](docs/research/provider-loading.md): why a shared file alone is insufficient.

External architecture research is filed under `docs/research/`. The [machine configuration example](docs/templates/machine.example.toml) is a proposal, not an installed configuration.

## Design boundary

Shared knowledge belongs here. `~/.jarvis` holds device paths, machine gotchas, caches, and local runtime state. The target codebase remains a sibling checkout and owns its detailed specifications, source code, checks, and deployment configuration.

Knowledge is not authorization. A memory about a previous action does not authorize repeating it. Policies and recommendations in this seed are labeled so a future agent can distinguish them.

## Machine initialization skill

The [machine-init skill](skills/machine-init/SKILL.md) sets up indexed repository
checkouts under `~/Documents/git`, adds the `awake` and `sleepy` Bash aliases,
and registers T3 projects when its tools are available on the target machine.
It supports local setup and execution on an explicitly selected remote host.

Install the `skills/machine-init` folder into your agent's skills directory
(for Codex, `~/.codex/skills/machine-init`), then invoke `$machine-init` or
`/machine-init` in a client that supports slash skill invocation. Jarvis owns
this machine-bootstrap skill; the separate `agent-skills` collection continues
to own its existing shared skills. The Python helper defaults to a dry run;
`--apply` performs setup. Installing the skill alone does not change `.bashrc`
or activate a sleep inhibitor.

## Lighthouse audit skill

The [lighthouse-audit skill](skills/lighthouse-audit/SKILL.md) (`/lighthouse-audit`
or `$lighthouse-audit`) asks which cataloged web repositories to skip, then
launches one Sonnet 5.5 T3 session per remaining repository across connected
environments that have the Jarvis project, or prints copy-paste prompts when
launching is unavailable. Each session audits a production build with the npm
`lighthouse` CLI, fixes attributable findings in a Treehouse worktree, and opens
a PR titled `chore(lighthouse): <date> audit fixes`. Each worker then waits for
CI, merges its own audit PR, and settles its T3 thread, under a scoped
authorization in [working agreements](context/working-agreements.md). Install it
the same way as machine-init. It grants no manual deploy or cleanup authority.
