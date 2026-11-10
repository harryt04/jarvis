# Node 26 portfolio migration plan

Status: proposed migration, 2026-11-10. This pass refreshed Jarvis from verified origin/main and performed read-only source reviews with three subagents. No application dependencies were installed and no application builds, runtime tests, deployments, or runtime changes were performed. No repository is certified compatible yet.

## Target and compatibility gates

Use the latest patched Node 26 LTS at implementation time. The official release index inspected for this plan lists 26.13.0 (Lithium); recheck it before pinning. Keep pnpm and committed pnpm lockfiles. Preserve existing pnpm versions initially where supported to isolate the runtime change. Avoid combining an unrelated framework major migration with a runtime-only change.

Upstream evidence checked 2026-11-10:

- [Node release index](https://nodejs.org/dist/index.json) and [26.13.0 LTS release](https://nodejs.org/en/blog/release/v26.13.0): official Linux binaries since Node 25 may require libatomic.
- [Node 26 changes](https://nodejs.org/en/blog/release/v26.0.0): removed writeHeader and legacy _stream_* modules, changed crypto behavior, new V8 and Undici versions, removed experimental transform-types flag. Native modules and custom loaders need targeted checks.
- [Node 25 changes](https://nodejs.org/en/blog/release/v25.0.0): Web Storage globals enabled; removed SlowBuffer, recursive rmdir option and legacy fs access constants. Review intermediate release changes from each repo's actual current major, including Node 23/24 for older baselines.
- [Corepack documentation](https://nodejs.org/download/release/v25.8.0/docs/api/corepack.html): bundled Corepack was removed starting with Node 25. Install pnpm or Corepack explicitly.
- [pnpm compatibility](https://pnpm.io/installation): Node 26 is listed as supported by pnpm 10. Verify each exact pinned version and its installation/bootstrap path; do not assume Corepack exists in the runtime image.
- [Vercel Node 26 announcement](https://vercel.com/changelog/node-js-26-lts-is-now-generally-available-on-vercel): builds and functions support 26. Broad Node engine ranges can select 26 on a later deployment. Verify the actual project configuration; source alone does not prove the live runtime.

## Execution and agent plan

1. Inventory and baseline: one worker per repository in bounded batches, initially at most three active workers and at most two concurrent heavy builds. Fetch and verify the actual default branch and SHA, read current instructions and open PRs, and preserve local work. Acquire or reuse a Treehouse task worktree and verify its base before any install or edit. Record manifest constraints, exact lockfile resolutions, runtime/CI/container pins, deployment build pack, OS/architecture and relevant integration boundaries.
2. Run the existing applicable checks on the declared current Node version using an unchanged frozen lockfile. Record independent exit codes; do not trust aggregate scripts that hide failures. Use isolated test databases and mocked external services. Missing secrets or test infrastructure are explicit limits, not a passing result.
3. Run the same checks on Node 26 with the same lockfile and pnpm version. Check dependency engine exclusions, peer conflicts, native binary availability, install-script approvals, removed APIs in application and resolved dependency source, ESM/CJS/custom loaders, SSR browser detection, crypto/auth, and fetch/TLS/streams. Rebuild native artifacts and use separate dependency/cache directories per Node major.
4. For failures unique to 26, record the exact error and owning dependency, verify upstream release notes/support, then select the smallest supported dependency update or code correction. Regenerate only the affected pnpm lockfile entries as practical. Run the baseline and Node 26 checks again. Never suppress engine checks or use a legacy OpenSSL flag as proof of compatibility. Separate substantial prerequisite framework changes into their own PR with an explicit dependency order.
5. Align package engines, developer version files, Node types where appropriate, all CI jobs, Docker build AND runtime stages, worker processes, build packs, bootstrap commands and active documentation. Test the production image itself on the deployment architecture; a passing host build alone is insufficient.
6. Each worker returns one tested PR, exact head SHA, commands/results, unresolved failures and deployment/rollback notes. Parent independently reviews riskier dependency/API changes; use a review subagent for substantial framework/native/auth changes, rather than automatically for every pin edit. Workers do not recursively delegate. No merge, deployment, or cleanup is implied by this plan.
7. Promotion, when authorized: verify live Coolify/Vercel settings and configured source branches, promote one app at a time, smoke test critical flows, inspect logs and retain the prior artifact and config for rollback. Coordinate shared Coolify capacity (historical cap two builds; recheck). Database schema changes should normally be unnecessary; if needed, plan rollback compatibility separately.

A repository passes only after clean frozen installation, applicable lint/type/unit/integration checks, production build, production start and critical-flow smoke tests on 26, plus deployment artifact validation. Track statuses as inventoried, baseline blocked, 26 failed, fixes planned, PR validated, or production verified. An engine range accepting 26 is only metadata evidence. Existing failures must be distinguished from regressions; unresolved required checks prevent a compatibility claim.

## Repository inventory and proposed order

The following source observations are planning evidence, not executed compatibility results. Refresh the default branch before implementation. Detailed specifications and fixes belong in the target repositories.

### Verify existing Node 26 configurations first

- **HairnThere**, `main@228ce286`: engines 26.x, nvmrc 26, pnpm 11.17; Next 16.4.4, React 19.3.1, sharp 0.35.5. Verification-only unless checks expose issues: lint, types, build, existing cinema checks and contact handling with isolated webhook configuration. Respect build-script allowlists for sharp/unrs. Newer Jarvis Treehouse/PR policy supersedes its historical direct-main exception.

### Pilot and conventional applications

- **Flowers**, `master@991bb0b4`: Node 24, pnpm 11.24; Next 16.2.6, React 19.2.4, MongoDB 7.2. Run CI and lint separately (CI omits lint), build/start and API validation with mocked email/Discord and disposable database. Verify sharp/SWC/oxide native packages on deployment architecture. Candidate pilot after existing-26 validation.
- **Grub Roulette**, `master@53e077a9`: Node 24, pnpm 11.24; Next 16.2.4, React 18.2, ESLint Next config 15. Baseline the framework/config mismatch before attributing failure to Node. Run types, unit/jsdom, build/start and Chromium flows with mocked Maps APIs; check SSR browser detection.
- **Portfolio**, `master@1ed509e2`: Node 24, pnpm 11.24; Next 16.2.0, React 18.3.1, MongoDB 6.21, ESLint Next config 15.5.14. Baseline mismatch, run CI and production start; smoke shared user/CRM endpoints using disposable data, not just page rendering.

### Legacy tooling and larger runtime jump

- **Rise Above Drone**, `master@9091e878`: Node 24, pnpm 11.24; Next 16.1.6, React 18.3.1. Existing lint uses removed `next lint`; repair the ESLint entry point/config as a baseline prerequisite. Run lint/build/start and landing/video smoke with dummy analytics configuration. No CI workflow was found in the inspected source.
- **Route Roulette**, `master@9ce9f8cc`: Node 24, pnpm 10.33.4; Next 14.2.35, SWC 14.2.33, MUI 5.15.15. Treat as higher uncertainty, not a demonstrated Node 26 failure. Validate install/lint/build/start and mocked geolocation/directions. Its AGENTS fences framework/MUI upgrades: if a framework major is necessary, report the specific dependency and request that scope change before proceeding.
- **Blockparty**, `master@e08de003`: Node >=22 <23, pnpm 10.17; Next 15.5.25, MongoDB 6.21, Vitest 5/Vite 8.2.2, sharp 0.35.4. Largest runtime jump. Run complete CI including coverage, seeded simulation and three-browser checks with disposable Mongo replica set. Exercise SSE/reconnect, transaction idempotency and tsx maintenance entry points against test data.

### Stateful applications and process-specific checks

All six below declare Node 24.x, nvmrc 24 and CI 24. pnpm is 11.24.0 except PantryIQ (9.15.4). Runtime/type/CI pins must move together. The versions below describe inspected local lockfiles. Only KanjiForge matched the remote default; for the others, current remote manifests/CI were rechecked but lockfile details must be refreshed before implementation.

- **KanjiForge**, local and remote `40ad8cee`: Next 15.5.21, Vitest 2.1.9/Vite 5.4.21, better-sqlite3 13.0.1 and sharp 0.34.5. Verify native SQLite/image installs, deck/pack checks, pack-refresh reproducibility, production build and Chromium/WebKit flows. Use disposable Postgres; startup runs migrations. N-API use does not remove the need for native installation tests.
- **MailFlow**, local `44b9546`, remote `10a07853`: Next 16.2.10, NextAuth 5 beta.31, Vitest 4.1.10/Vite 8.1.5 and jsdom 29.1.1. Run CI, coverage, Playwright, isolated OAuth/session refresh and mocked Gmail contracts, TTS/STT streaming/download checks. No real email sends.
- **PantryIQ**, local `bef9d5b`, remote `0371d827`: Next 15.5.23, Vitest 2.1.9/Vite 5.4.21, jsdom 30.0.1. CI uses bare `corepack enable` without explicit Corepack install: repair bootstrap for Node 26. Verify the exact pnpm 9 version on 26; keep a package-manager major change separate unless necessary. Run smoke, coverage/integration with disposable Postgres/Testcontainers, accessibility, charts, browser/UI gates and precompute worker.
- **Platter**, local `c36aa7a`, remote `1ed6d82`: Next 16.3.4, Vitest 3.2.7/Vite 7.3.6, sharp 0.35.4. Test web, realtime AND worker processes, custom import/tsx loader and tsup ESM output. Use disposable Mongo/Redis to exercise Socket.IO delivery, Agenda retries, HTTP/HTTPS imports and offline reconciliation.
- **Tokei**, local `8ae7219`, remote `2fb4859`: Next 16.1.6/React 18, Jest 30.2 with ts-jest 29.4.6, ESLint 8 with Next config 15.5.12. Baseline these mismatches. CI omits lint/build/E2E, so run those separately, plus auth/routine persistence against disposable Mongo and browser timer/audio checks.
- **VoiceBridge**, local `b27cd7d`, remote `13c9a3e`: Next 16.1.6/React 18, Vitest 3.2.6/Vite 7.3.6, jsdom 23.2, mongodb-memory-server 9.5.0. Run CI, auth/CRUD/AAC/rendering/upload checks; distinguish Mongo test binary architecture/download failures from Node regressions.

### Other active identities

- **RepoStaff**, remote `main@de0ee110`: already requires >=26.13.0 <27, pnpm 12.18.0, exact 26.13.0 Docker build/runtime and marketing CI. Next 16.4.5, React 19.3.1. Verification-only: frozen install, lint/types, standalone build, Playwright and container health. Explicitly run edge package typecheck/tests omitted by marketing CI. Cloudflare Workers compatibility is separate from Node tooling compatibility. Local checkout `4b45bf8` was behind the remote.
- **Personal project scaffold**, remote `master@b6bc0d1`, local `75fd5d3`: Node 24, pnpm 11.24.0, Next 16.1.6 local lock, React 18, Better Auth 1.5.4 range and MongoDB 6.21 range. Update pins/CI, run CI and production login/session smoke with disposable Mongo. No test runner exists. Verify SWC/sharp/esbuild and transitive Prisma binaries without broadening build-script allowlists; do not run live create-indexes. Remote manifest checked, remote lock not independently inspected.
- **Wiki**, remote `master@dab6f9a`, local `4722a88`: Node 24, pnpm 11.24.0, Next 16.2.5, React 19.2. No workflow or existing test suite found. Early pilot: frozen install, lint, typecheck, build/start and route/redirect/404 checks. Verify native dependencies; avoid capturing published personal content. Remote manifest checked; refresh remote lock before implementation.
- **Utility scripts**, local/remote `master@73252893`: no manifest/pin but a dependency-free Node ESM updater exists. Check syntax and dry-run on empty/disposable GIT_ROOT under 26; verify push-without-apply rejects. Never use this updater to perform the migration: it can commit/push across repositories and lacks required gates. No artificial package manifest needed.
- **Jarvis**, verified `main@aacaa47`: documentation/Python/shell procedures; no application Node runtime. No Node upgrade needed in the inspected source.
- **Lighthouse**, **agent-skills**, **prompts**: authenticated GitHub metadata returned 404 and usable cataloged checkouts were absent. Access-blocked inventory; do not infer deletion. Historical Lighthouse/Prompts briefs describe documentation, but current Node relevance cannot be confirmed. Do not inspect Lighthouse personal records or substitute unrelated installed skill trees.

Suggested order: verify HairnThere/RepoStaff, pilot Wiki/Flowers/scaffold, then Grub/Portfolio and the stateful apps, then Blockparty and Route Roulette. Repair Rise Above Drone lint and PantryIQ bootstrap alongside their baseline preparation. This order is based on verification complexity, not business priority. No independent project must wait for an unrelated project's fix; cap heavy work to available resources.

For Blockparty, Flowers, Grub Roulette, HairnThere, Portfolio, Rise Above Drone and Route Roulette, local checkouts were clean but behind the current remote defaults; the investigator separately read current remote manifests, pins, workflows and locks. Repeat scans in fresh task worktrees. Removed-API searches of inspected local app/tool sources found no direct matches, but this does not cover every resolved dependency or the newer remote source. Old Node 20/22 types in the six non-HairnThere projects should be reviewed during pin alignment.

## Scope and limits

All 21 active registry identities are accounted for, including repositories without a Node runtime and unavailable sources. Ants routes to RepoStaff and is not a separate migration. Deleted minizinc-web and ski-auto-parking stay excluded. Jarvis itself has no application Node runtime to upgrade. Do not add package manifests to documentation-only projects.

Historical hosting evidence: [Coolify guide](../integrations/coolify-mcp.md) identifies most apps on Coolify and Flowers on Vercel. Hosting settings and live process versions were not inspected in this pass. Read that guide before deployment work. Static findings cannot establish native ABI compatibility, integration success, or deployed behavior. Any unavailable source, stale local branch, missing infrastructure or unsupported dependency must remain visible in the worker's handoff.

## Source navigation

Remote manifest snapshots inspected by the investigators (short commit identifiers above resolve in their owning repositories):

[blockparty](https://github.com/harryt04/blockparty/blob/e08de003/package.json), [flowers](https://github.com/harryt04/flowers/blob/991bb0b4/package.json), [grub-roulette](https://github.com/harryt04/grub-roulette/blob/53e077a9/package.json), [hair-n-there](https://github.com/harryt04/hair-n-there/blob/228ce286/package.json), [portfolio](https://github.com/harryt04/portfolio/blob/1ed509e2/package.json), [rise-above-drone](https://github.com/harryt04/rise-above-drone/blob/9091e878/package.json), [route-roulette](https://github.com/harryt04/route-roulette/blob/9ce9f8cc/package.json), [kanji-forge](https://github.com/harryt04/kanji-forge/blob/40ad8cee/package.json), [mail-flow](https://github.com/harryt04/mail-flow/blob/10a07853/package.json), [pantry-iq](https://github.com/harryt04/pantry-iq/blob/0371d827/package.json), [platter](https://github.com/harryt04/platter/blob/1ed6d82/package.json), [tokei](https://github.com/harryt04/tokei/blob/2fb4859/package.json), [voice-bridge](https://github.com/harryt04/voice-bridge/blob/13c9a3e/package.json), [repo-staff](https://github.com/harryt04/repo-staff/blob/de0ee110/package.json), [personal-project-scaffolding](https://github.com/harryt04/personal-project-scaffolding/blob/b6bc0d1/package.json), [wiki](https://github.com/harryt04/wiki/blob/dab6f9a/package.json).

These links establish the manifest snapshot, not execution results or independently reviewed remote lockfiles where the inventory states otherwise.
