# Coolify deployment recovery: audit and results

Observed: 2026-11-07, approximately 22:39–22:41 UTC. Status of the initial snapshot: read-only audit and proposed recovery. Harry subsequently authorized diagnosing and fixing the failing deployments; the execution record below supersedes the earlier no-change status.

## Scope and evidence

Harry reports that the recent pnpm migration broke deployments, uses Coolify for deployments, enabled server/Caddy analytics, and queued fresh deployments. Authenticated MCP initialization succeeded against his supplied endpoint (Coolify 4.6.0, MCP server 0.3.0). The saved CLI contexts failed authentication; this audit used MCP read tools directly. The supplied token stayed outside Git. This is session access, not an installed cross-provider connection.

MCP inventory returned 17 applications, three databases, one reachable/usable server, and no applications or databases marked not running. All 17 apps were enumerated in one complete page. Per-app histories were queried independently (first 10; expanded to 30 for Wiki, MailFlow, Tokei, and Rise Above Drone). Missing success records within those windows do not mean an app never deployed successfully.

The fresh production batch has ten failed deployments, two completed deployments, and Platter production still building at the audit snapshot. Four beta apps have no fresh deployment in the returned history; PantryIQ beta returned no deployment history. Container status alone is not a health or release-freshness test.

Sixteen primary URLs returned HTTP 200 to GET. Rise Above Drone initially reset the connection; a follow-up HEAD returned HTTP 200 on both apex and www. No authenticated user journeys, database writes, alias-wide GET checks, or deployed-version confirmation were performed.

## Per-application snapshot

| Coolify application | Latest deployment | Commit | Finding |
| --- | --- | --- | --- |
| VoiceBridge | failed | b27cd7d5 | GitHub 429 fetching Nixpkgs |
| blockparty-beta | finished | 09c695f3 | No fresh redeploy in returned history |
| blockparty-prod | finished | f257da4c | Verify release and application behavior |
| grub-roulette | failed | 2a7bff3b | GitHub 429 fetching Nixpkgs |
| hair-n-there | finished | 5daf208e | Verify release and application behavior |
| harryt.dev | failed | 3c7fdcd1 | GitHub 429 fetching Nixpkgs |
| kanji-forge beta | finished | c6c90e35 | No fresh redeploy in returned history |
| kanji-forge prod | failed | 40ad8cee | GitHub 429 fetching Nixpkgs |
| mail-flow | failed | 44b9546e | GitHub 429 fetching Nixpkgs |
| pantry-iq beta | no history | unknown | No fresh redeploy in returned history |
| pantry-iq prod | failed | bef9d5b6 | GitHub 429 fetching Nixpkgs |
| platter-beta | finished | 3368ef15 | No fresh redeploy in returned history |
| platter-prod | in_progress | c36aa7a8 | Verify release and application behavior |
| riseabovedrone | failed | 994105a9 | GitHub 429 fetching Nixpkgs |
| route roulette | failed | e52d5b70 | GitHub 429 fetching Nixpkgs |
| tokei | failed | 8ae7219f | GitHub 429 fetching Nixpkgs |
| wiki | failed | 4722a88f | Corepack/pnpm install crash |

The production application named PantryIQ points to `harryt04/pantry-iq-landing`, while its beta points to `harryt04/pantry-iq`. Wiki points to `harryt04/markdown-webserver`. Resolve these live identities before editing; older Jarvis briefs/registry are snapshots and can be superseded by live source evidence.

## Confirmed failure mechanisms and limits

Nine fresh failures stop during Nixpacks setup while downloading a Nixpkgs archive from GitHub, with HTTP 429/rate-limit responses. This occurs before dependency installation. Simultaneous forced rebuilds are a plausible amplifier, not a proven sole cause. Grub Roulette, Route Roulette, and the PantryIQ landing app have successful history at the same commits now blocked by the download. Do not revert pnpm solely on this evidence; subsequent pnpm failures may still be hidden behind setup failure.

Wiki fails during `pnpm i --frozen-lockfile`: generated instructions install `corepack@0.24.1`, the runtime reports Node 22.19.0, and the error is `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING`. An earlier November 7 failure has the same signature. The current remote manifest requests Node `24.x` and `pnpm@11.24.0`. The build toolchain demonstrably differs from the manifest. Follow-up diagnosis found Wiki’s explicit build-time `NIXPACKS_NODE_VERSION=22` override (production and preview), explaining why the repository pin alone did not select Node 24. The generated Corepack/pnpm bootstrap also crashed. A controlled rebuild of the same commit using Railpack selected Node 24 and the pinned pnpm version and succeeded; the execution record below captures the rollout.

Blockparty production and HairnThere successfully used Railpack for the fresh batch; Wiki uses Nixpacks. This is a useful candidate path, not proof every app can switch safely.

## Detection and recovery sequence

1. Refresh the inventory and terminal status of this batch, especially Platter production. Record application/environment, actual repo and branch, deployment UUID, attempted SHA, last successful SHA/date, build strategy, failure phase, runtime health, and HTTP/critical-flow result. Extend history where needed; distinguish deployability failures from live outages. Preserve serving containers and do not cancel active work or roll back from build failure alone.
2. Investigate any live outage first. The Drone connection reset did not reproduce on HEAD, so confirm normal GET and its important page/form before classifying it as an outage. Check server CPU/memory/disk and proxy status if failures persist; no capacity cause was established by this audit.
3. For GitHub 429 failures, wait for throttling to clear and retry one application at a time with normal cache behavior. Do not repeat a fleet-wide forced rebuild. Reclassify any error revealed after setup succeeds. Keep frozen installs and committed locks; disabling them would conceal reproducibility problems.
4. Use Wiki as the toolchain pilot: resolve its current checkout and instructions; inspect manifest, lockfile, Node pins, build config, and the pnpm migration diff. Reproduce the reported install using the actual builder versions. Evaluate Railpack with the manifest's Node/pnpm versions, since it already worked for two apps. Coolify labels Railpack Beta, so validate generated commands, runtime image, port/binding, static assets, and app behavior before promotion. If it cannot meet the app's contract, use a repository-owned Dockerfile or narrowly scoped builder override with explicit versions. Select the smallest demonstrated fix; do not pin arbitrary replacement versions.
5. Apply the demonstrated fix only to apps with the same proven failure. Prefer beta environments before corresponding production changes, without assuming beta and production use identical branches or repositories. Keep each repository's pnpm lock and packageManager consistent; inspect lifecycle-script allowlists, native dependencies, and start commands if surfaced by logs. Use task branches/PRs except explicit repository delivery exceptions. Detailed specifications and fixes belong in each target repository.
6. Validate each candidate through a clean frozen install and relevant local checks, then the actual Coolify build and a successful replacement release. Verify the intended SHA, health, public pages/assets, and a minimal authorized user journey. For stateful apps check migration compatibility before release/rollback. Record evidence and rollback target. This plan does not authorize schema resets or data changes.
7. After the corrected releases, verify Caddy analytics attribution per app. A successful replacement must apply logging labels, then requests through Caddy must produce data. Redeploy the four betas separately if analytics is wanted there; this fresh production batch did not cover them. Close only when deployment, release freshness, application behavior, and analytics checks each have evidence.

## Analytics and PostHog decision

No application code or browser SDK is needed for Coolify traffic analytics. Sentinel reads JSON proxy access logs and produces aggregates. Caddy requires caddy-docker-proxy 2.9+; applications and service stacks must be redeployed after toggling collection. A failed build leaves the old resource without newly generated logging labels, explaining why “Redeploy to start logging” may remain after an attempted deployment. Successful deployment alone is insufficient: send traffic and confirm data. Installed proxy version and collection ingestion were not verified here.

Traffic analytics covers requests reaching Caddy, with bandwidth, visitor estimates, status codes, latency, paths, hosts, and referrer/device/geography breakdowns. Cached traffic served upstream without reaching Caddy, offline usage, and client-only interactions cannot be assumed to appear. CPU/memory metrics are separate.

Recommendation: trial Coolify as the default for simple hosted sites whose questions are about traffic and availability. Keep PostHog where custom business events, funnels, retention, session replay, feature flags, or experiments are used. Audit usage per repository before removal; replacing analytics must not break flags or app behavior. Compare usefulness over representative traffic, accounting for bots/assets/API requests and proxy caching, rather than expecting request counts to equal browser pageviews. Harry's statement that he may abandon PostHog is conditional, not a confirmed replacement policy.

Sources checked 2026-11-07:

- [Coolify traffic analytics](https://coolify.io/docs/core/observability/monitoring/traffic-analytics)
- [Coolify Railpack](https://coolify.io/docs/applications/builds/railpack)
- [Coolify Nixpacks](https://coolify.io/docs/applications/builds/nixpacks/overview)
- [PostHog product analytics](https://posthog.com/docs/product-analytics)
- [PostHog session replay](https://posthog.com/docs/session-replay)
- Read-only MCP inventory, per-app deployment histories, and capped redacted failure summaries; local audit evidence remains outside the repository under `~/.jarvis/audits/`.

## Authorized recovery execution

Harry explicitly requested diagnosis and fixes after reviewing the plan. Final verification: 2026-11-07 23:37 UTC. All ten targeted production applications successfully rebuilt and deployed the **same commits that failed in the initial batch**. No target application source or lockfile edits were needed.

Changed each failing application's Coolify build strategy from Nixpacks to Railpack. Wiki was the controlled pilot; its frozen install and application build passed with Node 24 and pnpm 11.24.0 before the remaining rollout. KanjiForge's earlier failure independently showed the same Node 22.19.0/Corepack 0.24.1 bootstrap crash. Railpack 0.43.0 selected repository-declared versions instead of the old Nixpacks toolchain. Node 24 was selected for all ten; Route Roulette retained pnpm 10.33.4, the PantryIQ landing site retained pnpm 9.15.4, and the other eight retained pnpm 11.24.0. The switch also avoided the Nixpkgs GitHub archive fetch that blocked nine fresh attempts.

Removed the redundant custom Corepack install overrides only from Grub Roulette and MailFlow, allowing Railpack's detected frozen pnpm install. Existing branches, base directories, domains, ports, build/start commands, and health-check settings were compared before/after and preserved. No manual environment-variable, database, or proxy changes were made. Existing Nixpacks-only version variables were not changed; they do not select Railpack's Node version. A future return to Nixpacks must revisit those overrides rather than restoring the known-broken Node 22 bootstrap.

Builds ran sequentially to limit load on the shared 8 GB server. Each corrected builder was exercised by an actual image build, including a forced rebuild for the nine apps after the pilot; serving releases remained until Coolify replaced them through its normal deployment flow. The three already successful production apps and four beta apps were left unchanged.

| Application | Deployed commit | Successful deployment |
| --- | --- | --- |
| wiki | `4722a88f` | [vmov1ierh0jatccte4i89hwa](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/g1warir83xtcssp6q47ym413/deployment/vmov1ierh0jatccte4i89hwa) |
| kanji-forge prod | `40ad8cee` | [r0fy8hc6ekgifdvahzcifl2q](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/o136yddat8uv39trxbaa0t10/deployment/r0fy8hc6ekgifdvahzcifl2q) |
| VoiceBridge | `b27cd7d5` | [x5jqdq7odvphiqibhnm13lut](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/dgs8oskg4o4gsc4swcog8kcc/deployment/x5jqdq7odvphiqibhnm13lut) |
| tokei | `8ae7219f` | [8objpdgqx0vradj48dvf2lht](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/es8w8g4484kc448skok4sco8/deployment/8objpdgqx0vradj48dvf2lht) |
| harryt.dev | `3c7fdcd1` | [rrvvvi8c6am2jojy9tulenhi](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/wg00sko4ck48w4www0g88gso/deployment/rrvvvi8c6am2jojy9tulenhi) |
| riseabovedrone | `994105a9` | [mvosmdnmpu3hjz4zzft9kwxw](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/qw4g800844w0kookck4wo8co/deployment/mvosmdnmpu3hjz4zzft9kwxw) |
| grub-roulette | `2a7bff3b` | [ywrtrejgfsyekiwyann4y872](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/u80osow/deployment/ywrtrejgfsyekiwyann4y872) |
| route roulette | `e52d5b70` | [txsw4un4pt4j939aidp8uu1o](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/v4c848kskowwco8ggggo0c00/deployment/txsw4un4pt4j939aidp8uu1o) |
| mail-flow | `44b9546e` | [bjoscqte5x0ldb8biix2tl3e](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/v11zlb8ierx51htgwhwivoqd/deployment/bjoscqte5x0ldb8biix2tl3e) |
| pantry-iq prod | `bef9d5b6` | [op42ahydgfubalzzlxl0seeh](https://coolify.harryt.dev/project/fk4gkkc/environment/gsw048o4cskk48k8g4ss808s/application/eksg4k8wgw8ss0gg8gck0440/deployment/op42ahydgfubalzzlxl0seeh) |

Verification:

- All ten deployment records report `finished`; each SHA matches its initially failing attempt.
- All 17 applications report running, and there are no open deployments at final inspection. Most report `running:unknown` because their health checks are disabled; this is not a claim that every feature was exercised.
- The ten recovered apps returned HTTP 200 on 13 website domains, with 26 sampled JavaScript/CSS asset requests also returning 200. The legacy VoiceBridge Clerk alias was excluded from the website smoke checks.
- Grub Roulette's existing health check passed on port 3001. Recent 60-line container-log samples for all ten recovered apps had no matches for the selected signatures: pnpm/bootstrap errors, missing modules, refused connections, port conflicts, missing auth secrets, unhandled rejections, or uncaught exceptions. This is a limited error-signature check, not exhaustive log analysis.
- Authenticated application journeys, email delivery, write flows, and analytics ingestion were not tested. Successful redeployments apply generated proxy labels; the final PantryIQ deployment explicitly logged a proxy-label change, but actual analytics collection still needs observation in Coolify.
- Documentation links, accidental private data, and whitespace were checked separately from live deployment verification. Credential values and raw infrastructure responses remain outside Git.

Transferable lesson: a package-manager migration's verification must include the deployment builder and its live runtime overrides, not only repository pins and local checks. In this incident, the migrated Node/pnpm declarations coexisted with an explicit Node 22 deployment override and an old Corepack bootstrap. Rebuilding the exact failing commits with an aligned toolchain demonstrated that configuration correction was sufficient.
