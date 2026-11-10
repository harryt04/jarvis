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
(for Codex, `~/.codex/skills/machine-init`; for Claude Code,
`~/.claude/skills/machine-init`), then invoke `$machine-init` or
`/machine-init` in a client that supports slash skill invocation. Claude Code
sessions started inside this checkout already discover both Jarvis skills
through the `.claude/skills -> ../skills` symlink, and load `AGENTS.md` through
the `CLAUDE.md` symlink. Jarvis owns
this machine-bootstrap skill; the separate `agent-skills` collection continues
to own its existing shared skills. The Python helper defaults to a dry run;
`--apply` performs setup. Installing the skill alone does not change `.bashrc`
or activate a sleep inhibitor.

## Lighthouse audit skill

The [lighthouse-audit skill](skills/lighthouse-audit/SKILL.md) (`/lighthouse-audit`
or `$lighthouse-audit`) asks which cataloged web repositories to skip, then
confirms the session model (default Sonnet 5.5), then launches one T3 session
per remaining repository across connected
environments that have the Jarvis project, or prints copy-paste prompts when
launching is unavailable. Each session audits a production build with the npm
`lighthouse` CLI, fixes attributable findings in a Treehouse worktree, and opens
a PR titled `chore(lighthouse): <date> audit fixes`, labeled `lighthouse-audit`,
with its Lighthouse results in the description. Each worker then waits for
CI, merges its own audit PR, and settles its T3 thread, under a scoped
authorization in [working agreements](context/working-agreements.md). Install it
the same way as machine-init. It grants no manual deploy or cleanup authority.
[`runs.json`](skills/lighthouse-audit/runs.json) records when the skill ran and
which repos it covered. Results come from the labeled PRs.

## Dependabot cleanup skill

The [dependabot-cleanup skill](skills/dependabot-cleanup/SKILL.md)
(`/dependabot-cleanup` or `$dependabot-cleanup`) scans every live
`harryt04/*` repository for open Dependabot PRs and classifies them as ready,
conflicting, failing, or pending. It then dispatches one subagent per
repository, at most two at a time to keep deployments paced. Each worker
resolves conflicts and fixes failing checks in a Treehouse worktree, pushes to
the Dependabot branch, and merges once CI passes, under a scoped authorization
in [working agreements](context/working-agreements.md). The skill keeps
rescanning until no new Dependabot PRs appear, then reports what merged and
why anything stayed open. Ask for a dry run to get the plan without any
writes. It grants no deploy, alert-dismissal, or cleanup authority.

## Shared upstream skills

`gh-axi` (GitHub through the `gh-axi` CLI) and `lavish` (reviewable HTML
artifacts through `lavish-axi`) are installed from upstream into
`.agents/skills/`, with versions pinned in `skills-lock.json`. Symlinks under
`skills/` expose them to Claude Code. Update them with the installer rather
than editing them by hand.

## Security review skill

The [security-review skill](skills/security-review/SKILL.md) coordinates bounded
subagents for blocked or failing Dependabot upgrades, application-code security
reviews, and read-only production configuration and deployment verification.
Routine package scanning stays with Dependabot. Workers use Treehouse task
worktrees and submit tested fixes as PRs for review; the skill grants no merge
or deployment authority. Install the `skills/security-review` folder like the
other Jarvis skills, then invoke `$security-review` with repositories and either
review-only or fix-and-PR scope. This is an on-demand procedure, not a scheduled
scan or an installed service.

## T3 session spawner skill

The [t3-session-spawner skill](skills/t3-session-spawner/SKILL.md)
(`/t3-session-spawner` or `$t3-session-spawner`) explains how to discover T3's
session-launch tools and start independent top-level sessions in Jarvis,
optionally balanced across linked machines. Workers reach sibling repositories
and use their Treehouse worktrees. It distinguishes session launches from
subagents, confirms model/effort and thread lifecycle choices before launch (manual pin reminder, confirmed auto-settle),
and documents bounded queue refill, partial failures, prompt-only fallback and local
`~/.dexter` storage for ad hoc plans and receipts. Actual availability depends
on the current harness; no sessions are launched by installing the skill.
