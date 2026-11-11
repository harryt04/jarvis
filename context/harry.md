# Harry Thomas

Reviewed: 2026-11-06. This is a seed, not a complete biography.

## Confirmed in the initiating request

- Harry Thomas is a Staff Software Engineer at Clozd. GitHub identity: `harryt04`.
- He wants Jarvis to be the usual starting point for planning, orchestration, and delegated routine work across his projects.
- He wants context to travel across AI providers, models, sessions, and machines, with the repository as the main durable store.
- He historically worked directly on `main` or `master` for many personal projects. He now wants better development hygiene as agents contribute.
- Almost all memory should be repository-level. Device-specific hardware, paths, and environment gotchas are the small local exception.
- Target repositories should be sibling folders of Jarvis. Folder names and repository identities are not always identical.
- Jarvis should learn his judgment and preferences so delegated work reflects how he would do it.

Follow-up instruction, 2026-11-06: learn HairnThere first; all remaining repositories have equal learning priority. Use subagents for the full portfolio, with sequential work acceptable when concurrency is limited. This authorizes this portfolio-learning pass, not permanent background agent use for every future task.

Subagent default from the same follow-up: use GPT-6.1 Sol with medium reasoning for new subagents, replacing the inherited xhigh setting. Apply this preference to future delegation unless Harry specifies otherwise or the requested provider/model is unavailable; report unavailability rather than silently substituting.

Source: Harry's initiating Jarvis conversation, 2026-11-06. This summary is newly authored; it is not a transcript.

## Confirmed meaning of memory requests, 2026-11-07

"Update Jarvis's memory" always means persist the understanding in long-term
repository storage and create or update a PR, so it survives switching machines.
A chat reply or machine-local note is insufficient. See the confirmed
[delivery agreement](working-agreements.md#confirmed-memory-request-delivery-2026-11-07).

Source: Harry's explicit clarification in the Jarvis conversation, 2026-11-07.

## Confirmed package-manager preference, 2026-11-07

Harry explicitly wants all his JavaScript repositories to use pnpm correctly with
a committed `pnpm-lock.yaml`. Scope includes package-manager pins, dependency
lock consistency, executable scripts, CI/deployment commands, and active setup
instructions. This does not select a universal pnpm/Node version or authorize
application reliability, authorization, or offline-sync changes. Repositories
without JavaScript manifests do not need artificial package files or lockfiles.

Source: Harry's correction in the Jarvis pnpm conversation, 2026-11-07. This
clarifies the task scope after Jarvis incorrectly expanded toward data-flow work.

## Confirmed tooling consistency preference, 2026-11-11

Harry wants to standardize tools where practical instead of using different
tools for the same purpose. In the Coolify builder discussion, he explicitly
authorized migrating the four remaining beta applications from Nixpacks to
Railpack, matching production. Use Railpack as the default automatic builder
for his Coolify apps; keep exceptions justified by application requirements.
This preference does not authorize unrelated migrations, merges, or deployments.

Source: Harry's explicit instruction in the Coolify builder conversation,
2026-11-11. Migration results are recorded in the
[Coolify integration guide](../docs/integrations/coolify-mcp.md).

## Confirmed by local/public sources

- Personal site: `https://harryt.dev`; GitHub: `https://github.com/harryt04`; LinkedIn is linked from the portfolio. His portfolio describes him as a staff engineer with a passion for separating signal from noise.
- His personal-project scaffold explicitly selects Next.js, TypeScript, Tailwind CSS, shadcn/ui, PostHog, Better Auth, and MongoDB. This is evidence of a starting preference, not a universal requirement. PantryIQ and KanjiForge are important PostgreSQL exceptions; MailFlow uses NextAuth.
- His projects include open-source consumer tools, small business websites, developer tooling, and private knowledge/planning repositories. Some knowledge repositories concern other people; ownership of the GitHub repository does not make their contents Harry's personal memory.

Sources: GitHub user/repository API observed 2026-11-06; `portfolio/app/page.tsx`; `portfolio/lib/portfolio-projects.ts`; `scaffolding/README.md`; corresponding project guidance. Revisions are in [the registry](../projects/catalog.json).

## Historically recorded, preserve scope

The Ants handoff dated 2026-09-29 records these as preferences from that planning session:

- Ask one self-contained question at a time, with context, plain-language options, and a recommendation.
- Explain business concepts plainly and let Harry judge customer/product fit.
- Use concise prose and avoid em dash characters in responses and product copy.
- Prefer his AXI CLIs when suitable and use familiar repository technologies unless another choice has a clear reason.
- Ants was described as a solo, part-time, bootstrapped effort aimed at profitability.

Source: `ants/docs/mvp/handoff.md`, sections 1–2, local revision recorded in the registry. This is a prior agent's attributed summary, not independently verified chat history. Apply these as starting guidance, with current instructions and evidence taking precedence. The Ants business constraints are project-specific; they are not a declaration that every future venture has the same constraints.

## Working inferences, not established preferences

- Offline use, accessibility, user-owned data, and understandable product behavior recur across several projects. This suggests useful questions to ask during product work; it is not a mandate for every product.
- The existing PR checks and detailed agent docs suggest the hygiene transition has already begun.

## Still unknown

- Maintenance budgets, which projects are paused, and business priority beyond the learning order above.
- Harry's general merge authority for agents. Existing policy authorizes task commits/pushes/PRs but does not grant blanket merging or deployment authority.
- Which harnesses and devices need first-class launch support beyond the current environment.
- A representative set of code reviews and PRs that show Harry's personal engineering judgment. Repository conventions alone are insufficient to reproduce it.

Keep sensitive employer details in their authorized source. This seed records Harry's employer and role as supplied; it does not import Clozd code, documents, or internal agent-farm designs.
