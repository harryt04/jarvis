# Stack and architecture defaults

## The rule

Confirmed, 2026-11-16: Harry uses his scaffold's stack "unless I have a really
good reason to use something else," and asked specifically for Better Auth,
Next.js and shadcn/ui components.

In the OpenSlots session the agent first proposed Postgres for booking
integrity. Harry pointed back to his stack, and the problem turned out to be
solvable on MongoDB with a unique index. Lesson: **solve the hard problem on
his stack first.** Propose a deviation only when you have tried and it truly
cannot be done well, present it as a decision with the reason, and accept no.

## The scaffold

`~/Documents/git/scaffolding`, GitHub `harryt04/personal-project-scaffolding`.
Read it live every time; this is a snapshot from 2026-11-16.

| Layer | Default | Notes |
| --- | --- | --- |
| Framework | Next.js 16, App Router, TypeScript strict | Uses `proxy.ts` exporting `proxy`, not `middleware.ts`. Signed-in routes live in an `app/(dashboard)/` group whose layout guards the session |
| UI | shadcn/ui look on [UI SDK](#ui-sdk) behaviors, Tailwind CSS v4, lucide-react, next-themes | Confirmed 2026-11-25: interactive components wrap `@ui-sdk/react`, not Radix UI or Base UI. On that date the scaffold was still a Tailwind v3 + shadcn `default` + Radix seed with an open pull request moving it to React 19, Tailwind v4 and UI SDK. Check whether it has merged; if not, a new app still starts on React 19 + Tailwind v4 + UI SDK |
| Forms | react-hook-form, zod | |
| Auth | Better Auth | `nextCookies()` must stay the last plugin. Do not pass `client` to `mongodbAdapter()`: that turns on transactions, which need a replica set |
| Database | MongoDB, native driver, no ORM | **Assume a standalone server with no multi-document transactions.** Indexes are created by a script, not at startup |
| Analytics | PostHog | Off unless a key is set. Keep it off public and embedded pages |
| Tooling | pnpm (pinned in `package.json`, committed `pnpm-lock.yaml`), Node 26, ESLint, Prettier | Corepack is not bundled with Node 26 |
| Tests | None in the scaffold | Add Vitest and Playwright when the app has logic worth protecting; say so as an adjustment |
| Hosting | Coolify, Railpack builder | Read `docs/integrations/coolify-mcp.md` in Jarvis before any deployment work |
| License | MIT | Confirmed 2026-11-16: he wants his projects MIT |

Known exceptions in his portfolio (evidence that exceptions exist, not
permission to add one): PantryIQ and KanjiForge use PostgreSQL; MailFlow uses
NextAuth. Read the project brief if a new app resembles one of them.


### UI SDK

Confirmed by Harry on 2026-11-25 as the default whenever an app uses shadcn/ui.
UI SDK is a behavior library from shadcn and Vercel, first released 2026-11-12:
keyboard, focus, popups, selection and ARIA in `@ui-sdk/core`, unstyled React
components in `@ui-sdk/react`, and an agent bridge that lets a browser agent
read and drive the page. Read on 2026-11-25 at `0.1.0-beta.17`; it is beta and
newer than most models' training data, so read it live every time.

- **Install** `@ui-sdk/react` and `@ui-sdk/core` at exact versions. It needs
  React 19 or newer; the styling setup in its docs uses Tailwind v4.
- **Read before writing.** The installed package carries its own docs and
  skill: `node_modules/@ui-sdk/react/docs/llms.txt` and
  `node_modules/@ui-sdk/core/skills/ui-sdk/SKILL.md`
  (`npx skills@latest add vercel-labs/ui --skill ui-sdk`). Do not infer the
  API from Radix or Base UI.
- **Components.** Each file in `components/ui/` wraps UI SDK parts, imported
  per component (`@ui-sdk/react/dialog`), and keeps the shadcn export names,
  props and Tailwind classes. App code imports from `components/ui/` only.
- **The shadcn CLI has no UI SDK base** (checked on shadcn 4.23.1: `base`,
  `radix`, `aria`). `shadcn add` for an interactive component brings Radix or
  Base UI back, so write those wrappers by hand. The CLI is still fine for
  tokens, themes and purely presentational pieces such as Card or Badge.
- **Agent bridge.** Mount `createAgent()` and `registerTools()` from
  `@ui-sdk/react/agent` once at the app root, with a deny-by-default `allow`
  policy in a small tested module. Irreversible actions get
  `data-agent-confirm`, sensitive fields `data-agent-secret`. Plan the policy
  in the TRD: which controls an agent may use is a product decision.
- **Known gaps on beta.17**, seen while adopting it in Harry's repositories:
  Select scroll-arrow buttons, Accordion Arrow-key movement between headers,
  indeterminate checkbox menu items, and ToggleGroup's single-select radio
  semantics. Sidebar, the React Hook Form wrapper, Resizable, DayPicker
  calendars and Embla carousels keep their own libraries. Name any component
  left on another library, with the tested reason, in the project's `AGENTS.md`.
- **Document it.** The new project's `AGENTS.md` gets a `## UI SDK` section
  covering the points above, because later agents will not know the library.

Not verified: the bridge against a browser with native WebMCP. Every adoption
on 2026-11-25 tested it through a stub.

## Adjustments that are normal

State each as an adjustment with the requirement that forces it:

- **Tailwind v4 + new-york** for any new app (the scaffold says so).
- **Geist fonts** in place of the scaffold's Inter, for the Vercel look.
- **A pnpm workspace** (`apps/web`, `packages/*`) only when something must be
  published or shared, such as npm components or a pure core library. A single
  app stays a single app.
- **Vitest and Playwright** when correctness matters.

## Architecture habits

These came out of OpenSlots and held up through its build.

- **Put the hard logic in a pure function.** No I/O, no reading the clock;
  inputs in, result out. Every surface that needs the answer calls it. Test it
  hard. (OpenSlots: `computeSlots`.)
- **Get integrity from a unique index, not from check-then-write.** Without
  transactions, model the contested resource so a duplicate-key error is the
  conflict signal, then roll back what you inserted.
- **Put every outside service behind a small interface with an in-memory
  fake.** This is what makes a no-credentials development mode and end-to-end
  tests possible. OpenSlots's `pnpm run dev:fake` (in-memory MongoDB, fake
  calendar, test sign-in) was worth building early; plan one in slice 0 or 1.
- **Scope every signed-in query to the owner in one place.** One function
  returns the session and the current workspace; pages and actions get their
  workspace only from it. Require a test that one user cannot reach another's
  data.
- **Fail closed when an integration is broken**, and show that state loudly in
  the UI. Draw that state in the spec.
- **Public endpoints** get a publishable key, an allowed-origin check, zod
  validation with length limits, and a rate limit stored where all instances
  can see it.
- **Tokens for the public are random, single-purpose and stored hashed.**
- **Secrets only in environment variables**, documented in `.env.example`.
- **If it is meant to be self-hosted:** Dockerfile, `docker-compose.yml`, a
  step-by-step self-host guide, and an optional sign-in allowlist.
- **If it publishes React components:** compiled, scoped CSS so hosts do not
  need Tailwind; shadcn-named CSS variables so a shadcn host can theme it;
  container queries so it adapts to the space it is given; the app itself
  consumes the package so there is only one copy of the UI.

## Honesty about what you know

Library option names and API details go stale. In the TRD, mark anything you
have not checked against current documentation as **Verify**, and assign it to
the slice that implements it, with the instruction to correct the TRD in the
same pull request.
