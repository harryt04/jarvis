# Coolify deployment burst failures and queue settings

Observed: 2026-11-09 evening Mountain time (2026-11-10 05:21–05:39 UTC). Scope: the single Coolify server `localhost` (Coolify 4.7.3) and its 18 applications in `web-hosting`. Harry asked for the concurrency and supersession changes below and for the failed deployments to be investigated; this record covers that task only.

## What failed

The Lighthouse-audit fan-out merged PRs into many repositories within minutes. Each merge fired a GitHub webhook deployment, so about 13 builds hit one server at once. Eight failed:

| Application | Evidence |
| --- | --- |
| mail-flow | `pnpm install` failed with `ResourceExhausted … cannot allocate memory`; npm requests took 30–37 s |
| route roulette | `next/font/google` (Roboto in `src/theme.ts`) threw `Cannot read properties of null (reading '1')`, so the Google Fonts CSS fetch came back malformed. The merged PR did not touch fonts, and the same code built on 2026-11-07 |
| VoiceBridge, repo-staff, wiki | Status `failed`, no log summary, no `finished_at`, all last updated at the same second (05:39:11 UTC) |
| platter-prod, hair-n-there, pantry-iq prod | Log stops at "Building docker image with Railpack", no error line, ended with the same group |

Server metrics: about 10.4 GB RAM total, about 5.3 GB used at idle, peaking near 7 GB during the burst (5-minute buckets, so they hide short spikes). CPU reached about 57%. The likely cause is memory and network exhaustion from too many simultaneous builds, not regressions in the merged code. The 2026-11-07 [recovery](coolify-deployment-recovery-2026-11-07.md) also followed a burst of about 13 queued deployments.

## Settings changed

- Server `localhost`: `concurrent_builds` went from 3 to **2** (`manage_server` update; read back as 2). `deployment_queue_limit` stays 25 and `dynamic_timeout` stays 3600.
- All 18 applications: `is_auto_cancel_building_deployments_enabled` went from false to **true** (REST `PATCH /api/v1/applications/{uuid}`; read back under `.settings`). `is_auto_cancel_queued_deployments_enabled` was already true on every app.

Together, a newer webhook, API, or MCP deployment of the same app cancels older queued *and* still-building ones. Coolify's `cancel_previous` documentation on the MCP `deploy` tool says a deployment that has started replacing containers always finishes, and manual, restart, and rollback deployments are never cancelled. Coolify already runs at most one deployment per application at a time.

Agent fan-outs that merge into many repositories still queue one build per app. With concurrency 2, those builds run two at a time instead of all at once.

## Recovery

The burst also crashed the Coolify server, so it was unclear which apps were running their latest commit. At Harry's request, all 14 production apps were queued for a **forced (no-cache) rebuild** with `cancel_previous: building`. That cancelled the earlier non-forced recovery deployments still in flight. Results, 2026-11-10 05:52–06:20 UTC:

- All 14 finished. Each deployed commit matched its GitHub branch head at queue time: VoiceBridge `13c9a3e`, blockparty-prod `e08de00`, grub-roulette `53e077a`, hair-n-there `228ce28`, harryt.dev `1ed509e`, kanji-forge prod `40ad8ce`, mail-flow `10a0785`, pantry-iq prod `0371d82`, platter-prod `1ed6d82`, repo-staff `9158f2a`, riseabovedrone `9091e87`, route roulette `9ce9f8c`, tokei `2fb4859`, wiki `dab6f9a`.
- Every primary URL returned HTTP 200 to a GET following redirects, and every container reported `running`. No user journeys or authenticated flows were tested.
- Server memory stayed between 4.1 and 6.9 GB. route roulette's Google Fonts build step succeeded under normal load, which supports the transient-network reading.
- One 45-second poll sample showed three deployments `in_progress` while the limit was 2. It may have been an old deployment still finishing container replacement (which is never cancelled), or a counting artifact. It was not investigated further.

Beta apps were not redeployed in this task.

## Follow-ups (proposed, not done)

- If route roulette's Google Fonts fetch fails again under normal load, self-host Roboto (`next/font/local` or `@fontsource/roboto`) so the build no longer needs the network.
- With about 5 GB already used at idle, two concurrent Next.js builds are the practical ceiling. Lower to 1, or add build-container memory limits, if `cannot allocate memory` returns.
