# Project knowledge seed

Original discovery: 2026-11-06. Availability refreshed 2026-11-07: 18 repositories still resolve. Shared agent skills, Lighthouse, and Planning prompts are unavailable (HTTP 404), not confirmed deleted. Harry confirmed deleting MiniZinc Web and Ski Auto Parking; they are excluded from routing, tasks, and recommendations. Their detailed briefs have been removed. The other notes retain their original observation scope. This is an orientation pass, not a code audit, production health check, or project-priority ranking. Runtime state and remote default branches must be rechecked before work.

[Machine-readable registry](catalog.json) records source revisions, origin aliases, entry points, and whether the observed checkout had changes. Folder names below are discovery hints; configured machine paths take precedence. A missing local source is called out explicitly.

| Project | GitHub repository | Local discovery | Purpose |
| --- | --- | --- | --- |
| Shared agent skills | [harryt04/agent-skills](https://github.com/harryt04/agent-skills) | `~/.agents/skills` | Harry's synced agent skill collection. |
| Ants | [harryt04/ants](https://github.com/harryt04/ants) | `../ants` | AI developer-farm product planning. |
| Blockparty | [harryt04/blockparty](https://github.com/harryt04/blockparty) | `../blockparty` | Private multiplayer property board game. |
| Sunshine Flower Bar | [harryt04/flowers](https://github.com/harryt04/flowers) | `../flowers` | Flower gifting brand, landing page, subscriptions and inquiries. |
| Grub Roulette | [harryt04/grub-roulette](https://github.com/harryt04/grub-roulette) | `../grub-roulette` | Random local restaurant discovery. |
| HairnThere | [harryt04/hair-n-there](https://github.com/harryt04/hair-n-there) | `../hair` | House-call hairdresser business website. |
| Jarvis | [harryt04/jarvis](https://github.com/harryt04/jarvis) | `../jarvis` | Portable digital assistant context and memory. |
| KanjiForge | [harryt04/kanji-forge](https://github.com/harryt04/kanji-forge) | `../kanji-forge` | Offline-first Japanese kanji/vocabulary study PWA. |
| Lighthouse | [harryt04/lighthouse](https://github.com/harryt04/lighthouse) | `../lighthouse` | Elisabeth's private continuity knowledge base. |
| MailFlow | [harryt04/mail-flow](https://github.com/harryt04/mail-flow) | `../mail-flow` | Resumable hands-free Gmail listening and voice commands. |
| PantryIQ | [harryt04/pantry-iq](https://github.com/harryt04/pantry-iq) | `../pantry-iq` | Explainable restaurant operational decision support. |
| Personal project scaffold | [harryt04/personal-project-scaffolding](https://github.com/harryt04/personal-project-scaffolding) | `../scaffolding` | Harry's default web application starter. |
| Platter | [harryt04/platter](https://github.com/harryt04/platter) | `../platter` | Shared recipe-to-grocery planning PWA. |
| Harry's portfolio | [harryt04/portfolio](https://github.com/harryt04/portfolio) | `../portfolio` | Portfolio/resume and shared user/CRM API endpoints. |
| Planning prompts | [harryt04/prompts](https://github.com/harryt04/prompts) | `../prompts` | Reusable product, requirements, and orchestration templates. |
| Rise Above Drone | [harryt04/rise-above-drone](https://github.com/harryt04/rise-above-drone) | `../rise-above-drone` | Drone photography website. |
| Route Roulette | [harryt04/route-roulette](https://github.com/harryt04/route-roulette) | `../route-roulette` | Random scenic-drive planning. |
| Tokei | [harryt04/tokei](https://github.com/harryt04/tokei) | `../tokei` | Multi-timer and routine workspace for kitchens. |
| Utility scripts | [harryt04/utility-scripts](https://github.com/harryt04/utility-scripts) | `../utility-scripts` | Personal shell automation. |
| VoiceBridge | [harryt04/voice-bridge](https://github.com/harryt04/voice-bridge) | `../voicebridge` | Visual AAC communication tools for autistic people and families. |
| Harry's wiki | [harryt04/wiki](https://github.com/harryt04/wiki) | `../wiki` | Markdown publication server with multiple content spaces. |

## Reading briefs

For deeper implementation knowledge, consult the [source learning pass](briefs/README.md). The inventory notes below remain the original orientation snapshot; a source brief identifies the newer evidence and any correction.

These capture the first files to read and the traps worth remembering. Follow the target repository's current instructions before using an older brief.

### Shared agent skills

Checked out at ~/.agents/skills rather than a sibling. Existing custom/upstream skill sources should stay separately maintained.

Read the actual local skill index when available.

Evidence: local files at `45ebcde340a4` plus GitHub metadata.

### Ants

Local Git history exists without origin; GitHub repository has no default branch/commits in API metadata. Treat local-to-remote identity as provisional. Do not copy employer-derived notes.

Read locally: `docs/mvp/handoff.md`, `docs/mvp/ants-company-outline.md`, `docs/mvp/prompt.md`.

Evidence: local files at `4845e5cb6f03` plus GitHub metadata.

### Blockparty

pnpm workspace; Next.js, pure deterministic engine, MongoDB replica-set transactions, SSE. Server authority, capability separation, versioned game content. README/AGENTS content activation claims disagree.

Read: [AGENTS.md](https://github.com/harryt04/blockparty/blob/09c695f3fa91617a2b13340a9e19c1d4e3e83cd2/AGENTS.md), [README.md](https://github.com/harryt04/blockparty/blob/09c695f3fa91617a2b13340a9e19c1d4e3e83cd2/README.md), [docs/README.md](https://github.com/harryt04/blockparty/blob/09c695f3fa91617a2b13340a9e19c1d4e3e83cd2/docs/README.md), [docs/product/prd.md](https://github.com/harryt04/blockparty/blob/09c695f3fa91617a2b13340a9e19c1d4e3e83cd2/docs/product/prd.md), [docs/engineering/architecture.md](https://github.com/harryt04/blockparty/blob/09c695f3fa91617a2b13340a9e19c1d4e3e83cd2/docs/engineering/architecture.md).

Evidence: local files at `09c695f3fa91` plus GitHub metadata.

### Sunshine Flower Bar

Vercel, MongoDB, Resend, Discord. Brand doc governs UI/copy. Current ci script formats in place, omits lint, and uses semicolons that can mask a failed build.

Read: [AGENTS.md](https://github.com/harryt04/flowers/blob/2eed694c26f251e36c92578036d9377424d6af9b/AGENTS.md), [README.md](https://github.com/harryt04/flowers/blob/2eed694c26f251e36c92578036d9377424d6af9b/README.md), [company-brand.md](https://github.com/harryt04/flowers/blob/2eed694c26f251e36c92578036d9377424d6af9b/company-brand.md), [lib/validation.ts](https://github.com/harryt04/flowers/blob/2eed694c26f251e36c92578036d9377424d6af9b/lib/validation.ts).

Evidence: local files at `2eed694c26f2` plus GitHub metadata.

### Grub Roulette

Google Maps key server-side. Base UI preset differs from Radix assumptions. No Zustand despite old plans. Workflow exists without a root ci script.

Read: [AGENTS.md](https://github.com/harryt04/grub-roulette/blob/701e2424ad7467754074f5b556e93f2bd0beb169/AGENTS.md), [README.md](https://github.com/harryt04/grub-roulette/blob/701e2424ad7467754074f5b556e93f2bd0beb169/README.md), [package.json](https://github.com/harryt04/grub-roulette/blob/701e2424ad7467754074f5b556e93f2bd0beb169/package.json), [src/lib/restaurant-logic.ts](https://github.com/harryt04/grub-roulette/blob/701e2424ad7467754074f5b556e93f2bd0beb169/src/lib/restaurant-logic.ts).

Evidence: local files at `701e2424ad74` plus GitHub metadata.

### HairnThere

Explicit early-stage direct-main exception; no PR/test/Actions/Docker pipeline. Service and pricing rules stay in source docs.

Read: [AGENTS.md](https://github.com/harryt04/hair-n-there/blob/400832fbcec8779116e320f9928aa7267c2d5eed/AGENTS.md), [README.md](https://github.com/harryt04/hair-n-there/blob/400832fbcec8779116e320f9928aa7267c2d5eed/README.md), [docs/mountain-cinema.md](https://github.com/harryt04/hair-n-there/blob/400832fbcec8779116e320f9928aa7267c2d5eed/docs/mountain-cinema.md), [docs/elisabeth-revision-plan.md](https://github.com/harryt04/hair-n-there/blob/400832fbcec8779116e320f9928aa7267c2d5eed/docs/elisabeth-revision-plan.md).

Evidence: local files at `400832fbcec8` plus GitHub metadata.

### Jarvis

Planning and seed only; unborn local checkout, no origin.

Read locally: `README.md`, `docs/setup-plan.md`.

Evidence: GitHub metadata and initiating request; no committed local source revision.

### KanjiForge

Local SQLite/OPFS plus PostgreSQL/Drizzle server. Account-scoped offline runtime and outbox. Electric is optional, snapshot sync default. Code and datasets have separate licenses.

Read: [AGENTS.md](https://github.com/harryt04/kanji-forge/blob/c6c90e354db9cb4605cf7d46a95eccf57d261adf/AGENTS.md), [README.md](https://github.com/harryt04/kanji-forge/blob/c6c90e354db9cb4605cf7d46a95eccf57d261adf/README.md), [docs/implemented-already.md](https://github.com/harryt04/kanji-forge/blob/c6c90e354db9cb4605cf7d46a95eccf57d261adf/docs/implemented-already.md), [docs/FEATURE-PARITY.md](https://github.com/harryt04/kanji-forge/blob/c6c90e354db9cb4605cf7d46a95eccf57d261adf/docs/FEATURE-PARITY.md), [docs/ARCHITECTURE.md](https://github.com/harryt04/kanji-forge/blob/c6c90e354db9cb4605cf7d46a95eccf57d261adf/docs/ARCHITECTURE.md).

Evidence: local files at `c6c90e354db9` plus GitHub metadata.

### Lighthouse

Separate person's sensitive records. Record project boundary only; targeted reading requires the task and source privacy rules. No wholesale import into Harry context.

Read: [AGENTS.md](https://github.com/harryt04/lighthouse/blob/6602cddf1c025653c2665d8b88b19b810f322653/AGENTS.md), [README.md](https://github.com/harryt04/lighthouse/blob/6602cddf1c025653c2665d8b88b19b810f322653/README.md).

Evidence: local files at `6602cddf1c02` plus GitHub metadata.

### MailFlow

NextAuth Google OAuth, MongoDB, OpenAI voice/cleanup. Old planning provider choices are historical. Do not manipulate a real inbox during general discovery.

Read: [AGENTS.md](https://github.com/harryt04/mail-flow/blob/bde567c4c80818ff08e82b64a503847e75889975/AGENTS.md), [README.md](https://github.com/harryt04/mail-flow/blob/bde567c4c80818ff08e82b64a503847e75889975/README.md), [docs/README.md](https://github.com/harryt04/mail-flow/blob/bde567c4c80818ff08e82b64a503847e75889975/docs/README.md), [docs/DECISION-TREE.md](https://github.com/harryt04/mail-flow/blob/bde567c4c80818ff08e82b64a503847e75889975/docs/DECISION-TREE.md), [docs/ARCHITECTURE.md](https://github.com/harryt04/mail-flow/blob/bde567c4c80818ff08e82b64a503847e75889975/docs/ARCHITECTURE.md).

Evidence: local files at `bde567c4c808` plus GitHub metadata.


### PantryIQ

Next.js, PostgreSQL, Drizzle. Money uses integer/decimal rules, business-day boundaries matter, email is auth plumbing. Legacy audit describes a replaced codebase.

Read: [AGENTS.md](https://github.com/harryt04/pantry-iq/blob/63c7ebfeee4f4fe68a139beba9ba44568f05c8eb/AGENTS.md), [README.md](https://github.com/harryt04/pantry-iq/blob/63c7ebfeee4f4fe68a139beba9ba44568f05c8eb/README.md), [docs/INDEX.md](https://github.com/harryt04/pantry-iq/blob/63c7ebfeee4f4fe68a139beba9ba44568f05c8eb/docs/INDEX.md), [docs/tech-stack.md](https://github.com/harryt04/pantry-iq/blob/63c7ebfeee4f4fe68a139beba9ba44568f05c8eb/docs/tech-stack.md), [docs/mvp-scope-and-decisions.md](https://github.com/harryt04/pantry-iq/blob/63c7ebfeee4f4fe68a139beba9ba44568f05c8eb/docs/mvp-scope-and-decisions.md).

Evidence: local files at `63c7ebfeee4f` plus GitHub metadata.

### Personal project scaffold

Next.js, TypeScript, Tailwind/shadcn, PostHog, Better Auth, MongoDB. Existing next-lint script and dependency compatibility need verification before reuse.

Read: [AGENTS.md](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/AGENTS.md), [README.md](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/README.md), [package.json](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/package.json).

Evidence: local files at `9f5a87cc9938` plus GitHub metadata.

### Platter

Next.js, MongoDB, Better Auth, Dexie offline state; web, realtime, and worker processes. Read current scope before extending it.

Read: [AGENTS.md](https://github.com/harryt04/platter/blob/3368ef15ab2739e88ec0963d01bd6c58a3c4a2ec/AGENTS.md), [README.md](https://github.com/harryt04/platter/blob/3368ef15ab2739e88ec0963d01bd6c58a3c4a2ec/README.md), [docs/mvp/prd.md](https://github.com/harryt04/platter/blob/3368ef15ab2739e88ec0963d01bd6c58a3c4a2ec/docs/mvp/prd.md), [docs/mvp/architecture.md](https://github.com/harryt04/platter/blob/3368ef15ab2739e88ec0963d01bd6c58a3c4a2ec/docs/mvp/architecture.md), [docs/DESIGN.md](https://github.com/harryt04/platter/blob/3368ef15ab2739e88ec0963d01bd6c58a3c4a2ec/docs/DESIGN.md).

Evidence: local files at `3368ef15ab27` plus GitHub metadata.

### Harry's portfolio

Contains more than static portfolio pages. Shared endpoints and analytics need care; app listings are evidence of configured URLs, not uptime.

Read: [AGENTS.md](https://github.com/harryt04/portfolio/blob/69919df4dfadb8376e7ecbd917e291f0b5373588/AGENTS.md), [README.md](https://github.com/harryt04/portfolio/blob/69919df4dfadb8376e7ecbd917e291f0b5373588/README.md), [lib/portfolio-projects.ts](https://github.com/harryt04/portfolio/blob/69919df4dfadb8376e7ecbd917e291f0b5373588/lib/portfolio-projects.ts), [app/api/user/route.ts](https://github.com/harryt04/portfolio/blob/69919df4dfadb8376e7ecbd917e291f0b5373588/app/api/user/route.ts).

Evidence: local files at `69919df4dfad` plus GitHub metadata.

### Planning prompts

Reference templates before inventing replacements; distinguish historical orchestration guidance from the active harness contract.

Read: [app-outline-template.md](https://github.com/harryt04/prompts/blob/2948559685a99f0be5ef760280d1d2d2f100ade6/app-outline-template.md), [PRD-TEMPLATE.md](https://github.com/harryt04/prompts/blob/2948559685a99f0be5ef760280d1d2d2f100ade6/PRD-TEMPLATE.md), [TRD-TEMPLATE.md](https://github.com/harryt04/prompts/blob/2948559685a99f0be5ef760280d1d2d2f100ade6/TRD-TEMPLATE.md), [ORCHESTRATION-TEMPLATE.md](https://github.com/harryt04/prompts/blob/2948559685a99f0be5ef760280d1d2d2f100ade6/ORCHESTRATION-TEMPLATE.md).

Evidence: local files at `2948559685a9` plus GitHub metadata.

### Rise Above Drone

Local origin uses old hizzy-drone name; GitHub API redirects to rise-above-drone. Thin docs; no root agent guidance found.

Read: [README.md](https://github.com/harryt04/rise-above-drone/blob/817f4fd7c38583bfa2c1829839fc86c171ba2527/README.md), [package.json](https://github.com/harryt04/rise-above-drone/blob/817f4fd7c38583bfa2c1829839fc86c171ba2527/package.json).

Evidence: local files at `817f4fd7c385` plus GitHub metadata.

### Route Roulette

Next.js 14, Material UI, Google Maps. This is not the Tailwind/shadcn scaffold. No root agent guidance or PR workflow found.

Read: [README.md](https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/README.md), [package.json](https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/package.json).

Evidence: local files at `61e5068ab7c8` plus GitHub metadata.


### Tokei

Next.js, MongoDB, Better Auth. Jest/Playwright scripts exist; baseline still needs execution and old next-lint command needs validation.

Read: [AGENTS.md](https://github.com/harryt04/tokei/blob/e7eff44c13259900a5a789bb8f9d2458d6dfb89b/AGENTS.md), [README.md](https://github.com/harryt04/tokei/blob/e7eff44c13259900a5a789bb8f9d2458d6dfb89b/README.md), [package.json](https://github.com/harryt04/tokei/blob/e7eff44c13259900a5a789bb8f9d2458d6dfb89b/package.json).

Evidence: local files at `e7eff44c1325` plus GitHub metadata.

### Utility scripts

Historical update script commits and pushes across projects and references absent legacy directories. Inventory only; do not run as a hygiene migration.

Read: [README.md](https://github.com/harryt04/utility-scripts/blob/ab8845b31b655f5d4e71ce4eb040e03fcf1724f4/README.md), [update-packages.sh](https://github.com/harryt04/utility-scripts/blob/ab8845b31b655f5d4e71ce4eb040e03fcf1724f4/update-packages.sh).

Evidence: local files at `ab8845b31b65` plus GitHub metadata.

### VoiceBridge

Next.js, MongoDB native driver, Better Auth, React Query. Detailed docs and PR CI exist; source package lint command differs from an older agent-doc description.

Read: [AGENTS.md](https://github.com/harryt04/voice-bridge/blob/375794356ede3610f3ebf807448de6edcbd53f99/AGENTS.md), [README.md](https://github.com/harryt04/voice-bridge/blob/375794356ede3610f3ebf807448de6edcbd53f99/README.md), [docs/index.md](https://github.com/harryt04/voice-bridge/blob/375794356ede3610f3ebf807448de6edcbd53f99/docs/index.md), [CODEBASE_MAP.md](https://github.com/harryt04/voice-bridge/blob/375794356ede3610f3ebf807448de6edcbd53f99/CODEBASE_MAP.md).

Evidence: local files at `375794356ede` plus GitHub metadata.

### Harry's wiki

All content/ files are published by design; never point this at Jarvis memory. Local old-name remote resolves to wiki through GitHub API. Preserve scoped CSS resets.

Read: [AGENTS.md](https://github.com/harryt04/wiki/blob/f0531a3748f2378537975bce04a2f96a3bd8353b/AGENTS.md), [CLAUDE.md](https://github.com/harryt04/wiki/blob/f0531a3748f2378537975bce04a2f96a3bd8353b/CLAUDE.md), [BRAND.md](https://github.com/harryt04/wiki/blob/f0531a3748f2378537975bce04a2f96a3bd8353b/BRAND.md), [lib/content.ts](https://github.com/harryt04/wiki/blob/f0531a3748f2378537975bce04a2f96a3bd8353b/lib/content.ts).

Evidence: local files at `f0531a3748f2` plus GitHub metadata.

## Adjacent sources

`../firstmate` belongs to `kunchenguid`, and `../rs-sdk` belongs to `MaxBittker`; neither is a Harry-owned project in this inventory. Extra `kanji-forge-*` folders are additional checkouts/worktrees of KanjiForge, not distinct products. Do not select one merely by its matching name.

`ants` has local files/history but no configured origin; confirm the intended association before publishing. `agent-skills` lives outside the sibling root. Deleted repositories are excluded from routing; see the registry tombstones.
