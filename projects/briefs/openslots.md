# OpenSlots

Observed 2026-11-16 from the local checkout and authenticated GitHub metadata. Identity: public, unarchived `harryt04/openslots`, default branch `main`, HEAD `a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03`, origin `https://github.com/harryt04/openslots.git`, clean working tree. Source links pin that revision. At this revision the repository holds **planning documents, a design spec and a license only**; there is no application code, manifest, lockfile or CI. Everything below about architecture is documented intent, not implemented or verified behavior. Re-review once the v1 build lands.

## Purpose, users and non-goals

OpenSlots is a free, MIT-licensed, self-hosted appointment booking service. An owner signs in with Google, links Google Calendar, defines services of different lengths and sets bookable hours; customers pick an open slot on a hosted page or through React components (`@openslots/react`) that the owner installs in another site. The motivating user is someone who runs several small businesses and does not want per-seat booking fees; one install serves several businesses. [PRD sections 1–3](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/PRD.md#L5-L20).

Explicitly out of v1: payments, several staff per business, calendars other than Google, email or SMS sent by OpenSlots, recurring or group bookings, customer accounts, teams and roles, a theme chooser and translations. [PRD section 4](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/PRD.md#L42-L44).

## Current state

Status on 2026-11-16: PRD and TRD marked "approved for v1 build"; an orchestrated, slice-by-slice build started the same day. Slice pull requests are evidence of progress, not of merged or deployed behavior; read live Git and PR state before relying on any slice. No deployment, npm package or Google Cloud client was observed.

## Planned architecture (documented intent)

- **Workspace.** pnpm workspace: `apps/web` (Next.js 16 App Router admin, hosted booking pages, public API), `packages/core` (`@openslots/core`: pure slot engine, zod schemas, shared types, no I/O), `packages/react` (`@openslots/react`: `BookingFlow`, `SlotPicker`, `ServiceList`, hooks, typed client). [TRD section 2](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/TRD.md#L24-L40).
- **Stack.** Harry's scaffold stack (Next.js, TypeScript strict, shadcn/ui, Better Auth, MongoDB native driver, PostHog, pnpm) started on Tailwind v4 and the new-york style rather than the scaffold's legacy Tailwind v3 setup, plus Vitest and Playwright. [TRD section 1](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/TRD.md#L7-L22).
- **Slot engine.** `computeSlots` is a pure function that takes rules, schedule, busy intervals and `now`, and returns UTC start instants per schedule-local date. The admin preview and the public API must both call it. [TRD section 4](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/TRD.md#L58-L83).
- **Booking write path.** MongoDB runs standalone with no multi-document transactions. Double booking is prevented by inserting one `slot_locks` document per 5 minute block under a unique `{businessId, block}` index; a duplicate-key error rolls the attempt back and returns `409 slot_taken`. Google free/busy is re-read immediately before confirming, then the event is created with the customer as attendee so Google sends the invitation. [TRD section 5](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/TRD.md#L85-L100).
- **Google.** Better Auth Google provider with offline access and calendar scopes; a `CalendarProvider` interface with a Google implementation over plain `fetch` and an in-memory fake for tests. Any auth failure marks the link `needs_reconnect` and the slots endpoint fails closed. Several items are marked **Verify** for the implementing slice. [TRD section 6](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/TRD.md#L102-L111).
- **Public API.** `/api/v1` keyed by a publishable key (`X-OpenSlots-Key`) with an allowed-origin check, rate limits stored in MongoDB, and hashed manage tokens. Admin queries are scoped to businesses the session's user owns. [TRD section 7](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/TRD.md#L113-L128).

## Durable gotchas and project-scoped decisions

These come from the repository's own `AGENTS.md` and the dated planning documents; they are project-scoped, not global policy.

- The stack is fixed. Do not add Postgres, an ORM, another auth library or another UI kit. Do not replace the `slot_locks` unique index with a read-then-write check. Nothing outside `packages/core` computes availability. The hosted pages consume `@openslots/react` from the workspace; there is one booking UI. [AGENTS.md rules](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/AGENTS.md#L14-L24).
- Colors come from tokens (theme "Voltage"), and any state shown with color also needs an icon, label or text decoration; no red versus green. The instructions give Harry's colorblindness as the reason and treat this as a hard requirement. [Design README](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/design/README.md#L19-L30).
- The design spec `docs/design/openslots-design.html` is the visual target, with screen IDs (`S1`–`S10`, `C1`) and numbered acceptance checks that pull requests cite.
- Each self-hoster needs their own Google Cloud OAuth client; one left in "Testing" expires refresh tokens after 7 days. The self-host guide must cover publishing it. [PRD risks](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/PRD.md#L73-L81).
- Merging, publishing to npm, deploying and repository settings changes need Harry's explicit approval. Work happens on task branches in isolated worktrees and ends in pull requests; never push to `main`.
- The orchestration plan restricts build agents to `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5` and `gpt-6.1-sol` at no more than medium reasoning, with cross-provider review per slice. This is scoped to the v1 build. [Orchestration plan](https://github.com/harryt04/openslots/blob/a826c5ed5a0f8a39d5dfc005994e44e1f0bd3e03/docs/ORCHESTRATION.md#L5-L23).

## Verification and delivery

No commands existed at the observed revision; `AGENTS.md` says the bootstrap slice fills in the Commands section (`dev`, `ci`, `test`, `e2e`, `create-indexes`) and warns against inventing commands that are not in `package.json`. Read the live `AGENTS.md` and `package.json` before running anything. Planned deployment is a Dockerfile and docker-compose for self-hosting, with Harry deploying on Coolify; nothing is deployed.

## Unknowns

Whether the TRD **Verify** items about Better Auth and Google scopes hold; the npm scope `@openslots` has not been confirmed as owned; no production instance, Google Cloud project or first integration exists yet.

## Task-to-reading map

| Task | Read first |
| --- | --- |
| Any change | `AGENTS.md`, then `docs/PRD.md` and `docs/TRD.md` |
| UI work | `docs/design/README.md` and the matching screen in `docs/design/openslots-design.html` |
| Slot math or booking correctness | TRD sections 4 and 5 |
| Google or auth | TRD sections 6 and 9 |
| Embedding or the npm package | TRD sections 7 and 8 |
| Coordinating the build | `docs/ORCHESTRATION.md` |

Review triggers: the v1 build merging, the first deployment, the first npm publish, or any change to the booking write path.
