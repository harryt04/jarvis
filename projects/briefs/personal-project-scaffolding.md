# Personal project scaffolding

Observed 2026-11-06. Source: `/Users/harry/Documents/git/scaffolding`, origin `https://github.com/harryt04/personal-project-scaffolding.git`, branch `master`, HEAD `9f5a87cc99384a8f925d55cd176098631f18a44b`. `git status --porcelain=v1` was empty before and after inspection: no dirty-file exceptions were observed. All source citations below refer to this pinned revision; repository inventory observations describe the inspected checkout. No remote freshness or deployment state was checked.

## Verified follow-up, 2026-11-07

The November 6 source snapshot below is historical. The default branch advanced to
`2e7a1fba9e3cd4594eeb0fabb45cb25f05336a93`, merging the pnpm migration and
Node 24 standardization. The current seed pins pnpm 11.24.0 and has a sole pnpm
lockfile. Do not repeat the npm migration based on the older snapshot.

[Follow-up PR #3](https://github.com/harryt04/personal-project-scaffolding/pull/3),
head `f140586226affa26df29b0d1c384d03631025c4e`, repairs Next 16 ESLint
configuration, adds generated route types/typechecking to CI, makes browser
PostHog optional, and replaces Gulp's cross-project database targeting with an
explicit single-environment index runner. Setup instructions now keep connection
strings in environment configuration. The unused server analytics helper still
requires a production key. PR #3 was confirmed merged on 2026-11-07; the implementation is now on the default branch.

Verification actually executed on Node 24.5.0/pnpm 11.24.0: fresh worktree install,
frozen-lockfile install, lint (one scoped warning in the legacy generated sidebar),
typecheck, production build without a browser analytics key using placeholder
localhost configuration, invalid-environment rejection before database access,
and whitespace checks. GitHub's `validate` check also passed on the PR head.
No live database/auth flow, index mutation, deployment, or UI behavior was tested.
The settings route and placeholder collection/index still need project-specific
review before this seed becomes a product; the tooling PR does not resolve them.

## Purpose and reusable intent

Harry describes this as his “blank slate” for personal projects, choosing Next.js, TypeScript, Tailwind, shadcn/ui, PostHog, Better Auth, and MongoDB ([README.md:1–9](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/README.md#L1-L9)). It supplies an authenticated shell and infrastructure conventions, not a finished product, domain schema, or deployment platform. These are project-scoped defaults, not evidence of a universal personal policy. Current metadata and sitemap still use scaffold branding; the unused landing component retains a waitlist link and beta copy (`app/layout.tsx:15–18`, `app/sitemap.ts:3–13`, `components/custom/landing-page.tsx:5–36`). Those are replacement material, not established product requirements.

Standing authority is `AGENTS.md`: authenticated pages belong in the dashboard group; Server Components are the default; shadcn primitives are regenerated rather than manually edited, except specified import corrections; formatting uses single quotes/no semicolons; collection types belong in `models/` (`AGENTS.md:49–84, 88–128, 150–159`). The models directory exists but contains no files. TypeScript enables strict checking while explicitly tolerating implicit any (`tsconfig.json:3–10`).

## Routing and the session boundary

The main read path is `/` → `app/(dashboard)/layout.tsx` → `auth.api.getSession({ headers: await headers() })` → redirect to `/login` if absent → sidebar shell and child content. The route group does not introduce a `/dashboard` URL. Home performs a second session lookup and renders the user's name or email, using a non-null assertion that relies on the layout guard ([app/(dashboard)/layout.tsx:12–29](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/app/%28dashboard%29/layout.tsx#L12-L29); `app/(dashboard)/page.tsx:4–13`). A future API or data mutation still needs its own authorization boundary; layout placement does not establish ownership checks for arbitrary endpoints.

`proxy.ts:8–23` only checks cookie presence and only redirects missing-cookie requests whose paths begin `/dashboard`. This does not cover the actual home URL, and no dashboard-prefix page appears in the tracked tree. Its own comments explicitly deny cryptographic validation; the layout performs the meaningful validation. The matcher includes API paths, but that does not make every API authenticated (`proxy.ts:26–33`).

A consequential mismatch: the sidebar advertises `/settings`, but `app/settings/page.tsx:1–14` is outside the guarded group and contains no session check. Today it returns only placeholder text, so inspection found no sensitive settings exposed; future settings data must not inherit an assumed sidebar-based protection. `/login` is intentionally public and renders `LoginCard` (`app/login/page.tsx:1–14`; `components/custom/app-sidebar.tsx:21–24`).

## Account creation, cookies, and Mongo ownership

`LoginCard` switches between signup and signin. It collects email/password and signup name, applies browser-required/email controls, calls `signUp.email` or `signIn.email`, requests callback `/`, displays returned errors, and pushes `/` on success (`components/custom/login-card.tsx:21–52, 60–103`). There is no custom schema validation or application-specific user provisioning in that path. The submit function has no exception handler/finally: a thrown request failure can bypass clearing loading, unlike an ordinary returned auth error.

The React client is an uncustomized `createAuthClient()` with named session/signin/signup/signout exports (`lib/auth-client.ts:1–5`). GET and POST at `/api/auth/[...all]` delegate directly to Better Auth (`app/api/auth/[...all]/route.ts:1–4`). The server enables email/password, creates its own MongoClient, selects `scaffolding-${NODE_ENV}`, and passes only the database into `mongodbAdapter`. `nextCookies()` is last, preserving the documented Set-Cookie integration for server actions/RSCs ([lib/auth.ts:6–27](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/lib/auth.ts#L6-L27)). Omitting the client argument to avoid transaction requirements is an explicit repository decision; the comments' particular Atlas-tier assertion was not independently verified. Do not silently change adapter options when copying this scaffold.

Signout calls the client and navigates to login on success (`components/custom/app-sidebar.tsx:29–35`). No custom user model, roles, tenant mapping, email verification/reset flow, or analytics identity reconciliation is wired in the inspected source. Better Auth owns auth persistence behind its adapter; library-internal schema, cookie defaults, and security controls were not inspected. `AGENTS.md:140–147` names `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`, Mongo connection string, and public analytics settings. Source explicitly validates Mongo presence, while secret/base-URL handling is delegated to the library. No environment values were read.

## Shared database and analytics conventions

Application queries are intended to use `getMongoClient()`: a module-local client and connection promise are reused, with missing connection configuration rejected at import (`lib/mongo-client.ts:1–24`). This is separate from the auth client by explicit policy (`AGENTS.md:152–155`), but shares its database-name convention. It is not a global hot-reload cache; a rejected connect promise is retained without retry reset. Collection registration currently contains only `scaffoldingCollection`; no application user/data query is implemented (`lib/mongo-client.ts:26–31`).

Root layout wraps all routes in PostHog and theme providers (`app/layout.tsx:26–44`). Browser analytics initializes only in production, uses same-origin `/ingest`, and captures pathname changes as `$pageview`; Next rewrites ingest traffic to US PostHog endpoints (`providers/posthogProvider.tsx:10–33`; `next.config.js:7–24`). There is no auth-linked `identify` or signout reset in the inspected call sites. Pageview deduplication against SDK defaults remains unverified.

Policy says the key is optional in development, but the provider throws for a missing key before checking production (`AGENTS.md:146`; `providers/posthogProvider.tsx:7–12`). Consequently importing the root provider requires the key even in dev. The separate server factory returns a capture-only no-op outside production, requires a key in production, and creates a fresh immediate-flush client using the configured host; no caller was found (`lib/posthog-server.ts:3–19`). This is a reusable helper awaiting integration, not evidence of server event delivery.

## Index generation and delivery limits

Index flow is manifest `create-indexes` → `npx gulp create-indexes` → `gulpfile.ts` → `createMongoDbIndexes`. The helper lists collections, creates a missing collection, and requests a non-unique ascending `blahId` index (`lib/mongo-utils.ts:6–29`). However, Gulp hardcodes **both `voicebridge-development` and `voicebridge-production`**, inconsistent with runtime `scaffolding-*` databases ([gulpfile.ts:1–7](https://github.com/harryt04/personal-project-scaffolding/blob/9f5a87cc99384a8f925d55cd176098631f18a44b/gulpfile.ts#L1-L7)). This is stale project-specific wiring, not a reusable migration contract. The README's advice to place a connection string in source is also unsafe to adopt as a requirement; the code already accepts an environment variable (`README.md:11–15`; `lib/mongo-client.ts:2–8`). No environment loader is explicit in the Gulp entry, and its TypeScript loading prerequisites remain unverified.

Node 24.x is declared. Actual scripts are `next dev`, `next build`, `next start`, `next lint`, Gulp indexes, and repository-wide Prettier (`package.json:5–14`). **`next lint` is a stale framework-incompatible command for Next 16**, not a verified lint pathway; the manifest pairs Next `^16.1.6` with eslint-config-next `^15.5.12` and legacy `.eslintrc.json` (`package.json:36, 53–54`; `.eslintrc.json:1–3`). No command was executed to reproduce this incompatibility. Policy additionally documents `npx tsc --noEmit` and explicitly says no test runner exists (`AGENTS.md:13–22`). The tracked inventory contains no CI workflow, Dockerfile, or provider deployment configuration: build then start is the available application contract, not proof of a working deployment. Runtime Mongo connectivity, production origins/cookies, analytics credentials, and framework compatibility remain deployment prerequisites.

## Reading map and review triggers

For routing work, read the dashboard layout, proxy, settings placement, and sidebar together. For account changes, read LoginCard → auth client → catch-all handler → auth server, retaining cookie-plugin ordering and reviewing database topology before changing adapter options. For persistence/index work, read mongo-client → mongo-utils → Gulp and reconcile database names before any execution. For telemetry/startup, read root layout → PostHog provider → Next rewrites, plus the unused server helper. Review this brief after route movement, auth-library upgrades, user-model introduction, index changes, analytics identity integration, or delivery configuration changes. This was static read-only research: no installs, builds, tests, application/service startup, provider actions, secrets, or source mutations occurred.
