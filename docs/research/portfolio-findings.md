# Portfolio learning: cross-project findings

Observed 2026-11-06. This is the parent synthesis of reviewed [source briefs](../../projects/briefs/README.md). It records navigation lessons and follow-up candidates from static investigation. No application builds, tests, services, accounts, or deployed behavior were exercised. The briefs carry the revision-pinned evidence and project-specific detail.

All 23 repositories received an independent brief. HairnThere started first; the remaining projects had equal priority. Investigations begun after Harry's model-setting correction used GPT-6.1 Sol at medium reasoning. Lighthouse was reviewed for operating structure only. Source revisions and scope limits belong to each brief, not a claim of exhaustive or live production expertise.

## Owner-confirmed deletions and availability, 2026-11-07

Harry confirmed deleting MiniZinc Web and Ski Auto Parking and asked Jarvis to
forget MiniZinc as noise. Both are excluded from project routing, recommendations,
and pnpm work; their detailed briefs and follow-up candidates have been removed.
The registry retains only minimal deletion markers to prevent rediscovery.

An authenticated inventory/API check found 18 other repositories still available.
`agent-skills`, `lighthouse`, and `prompts` return HTTP 404 and are absent from the
owner inventory; deletion versus transfer/access change is not established.
Their briefs remain historical and are excluded from active recommendations.

## Package-manager correction, 2026-11-07

An authenticated read-only inspection of current remote default-branch manifests,
root lockfiles, and selected workflows found that all 16 application repositories
already use a sole `pnpm-lock.yaml`. Earlier local npm observations were stale;
the November 6 briefs remain revision-scoped historical evidence. Avoid launching
another portfolio migration from those snapshots.

The scaffold already pins Node 24/pnpm 11.24.0 on its default branch. Its
[follow-up PR](https://github.com/harryt04/personal-project-scaffolding/pull/3)
repairs validation, startup, and index tooling; see its
[updated brief](../../projects/briefs/personal-project-scaffolding.md) for executed
checks and remaining limits. HairnThere's local manifest, lockfile, runtime files,
and instructions were consistent with its Node 26/pnpm 11.17.0 baseline at
`729e8c82388b85fd2f510ca79568e6e821fde7c0`; that inspection was static and did
not execute its install/build. Its distinct delivery policy remains in force.

Remaining package-manager follow-up candidates:

- KanjiForge: missing manager pin in [package.json](https://github.com/harryt04/kanji-forge/blob/d4c61c485b10d6837d26dac47c49607c275f6bfc/package.json) and pnpm 9 in [CI](https://github.com/harryt04/kanji-forge/blob/d4c61c485b10d6837d26dac47c49607c275f6bfc/.github/workflows/ci.yml) and [monthly refresh](https://github.com/harryt04/kanji-forge/blob/d4c61c485b10d6837d26dac47c49607c275f6bfc/.github/workflows/monthly-pack-refresh.yml), alongside the newer [build policy](https://github.com/harryt04/kanji-forge/blob/d4c61c485b10d6837d26dac47c49607c275f6bfc/pnpm-workspace.yaml).
- Rise Above Drone: removed Next 16 lint command in [package.json](https://github.com/harryt04/rise-above-drone/blob/994105a91d54621a6304cee3f2da7a840b1d170b/package.json).
- Flowers: [CI script](https://github.com/harryt04/flowers/blob/05adc99fa226c5bc1853e6e85ea2df9a2ed4ffb7/package.json) omits lint; its [workflow](https://github.com/harryt04/flowers/blob/05adc99fa226c5bc1853e6e85ea2df9a2ed4ffb7/.github/workflows/ci.yml) invokes that script.

These are source configuration observations,
not reproduced runtime failures. Preserve intentional version differences until
verified in each target repository. Deeper data-flow investigations listed below
remain candidates, not confirmed incidents. Maintenance tiers are still proposed;
Harry has not selected active, maintained, or parked status per project.

## Package-manager execution follow-up, 2026-11-07

Harry clarified that this task is pnpm correctness across repositories, not deeper
application reliability work. The earlier data-flow candidates remain separate
research observations and are not this task's implementation scope.

A final read-only, revision-pinned remote audit compared dependency,
devDependency, and optionalDependency specifiers against lock importers for every
accessible application, including Blockparty's nested workspace packages. Every
specifier matched, with no competing npm/Yarn/Bun lockfiles. This is static
manifest/lock verification, not an executed install/build for every application.
Machine-local detailed audit evidence remains outside this repository.

- Scaffold [PR #3](https://github.com/harryt04/personal-project-scaffolding/pull/3) is now merged; its GitHub validation passed.
- KanjiForge [PR #18](https://github.com/harryt04/kanji-forge/pull/18), head `aea319b7c24cfecc62f547c813e81a34292ee005`, pins pnpm 11.24.0, aligns both workflows and active commands/docs, and preserves its existing lockfile. A fresh frozen install, lint/worker types, build, and ten pack tests passed locally. GitHub smoke, unit coverage, Chromium, WebKit, and aggregate checks passed. Its default branch still lacks the pin until this PR merges.
- Utility scripts [PR #2](https://github.com/harryt04/utility-scripts/pull/2) replaces npm update commands with pnpm and routes the legacy shell entry through the dry-run-first updater. Syntax and isolated dry-run verification passed; no actual dependency updater ran.
- Wiki [PR #3](https://github.com/harryt04/wiki/pull/3) align remaining active setup/skill commands. This is an instruction-only change verified by diff/whitespace checks.
- Blockparty's pnpm-only CI/docs patch is preserved locally. Its frozen pnpm install passed on Node 22.23.4/pnpm 10.17.0. Its required gate passed formatting/typecheck/lint, then reported application-test failures and stopped progressing; the test run was interrupted. Repository policy prohibits committing/pushing while the gate fails, so an explicit exception is pending. The patch does not change application behavior.

The accessible owner inventory changed during this session. Previously cataloged
`prompts`, `agent-skills`, and `lighthouse` no longer resolve through the
authenticated API or owner list; deletion, transfer, or access change is unknown. The remaining unavailable-source briefs remain historical; the two owner-confirmed deletions supersede the earlier availability uncertainty. Do not recreate,
unarchive, or substitute remotes from those snapshots. The current accessible
non-application repositories have no manifest needing a lock; Ants' remote is
empty. Minor stale comments and historical logs are not active installation paths.

## How Jarvis should use this knowledge

**Resolve the project before applying a convention.** Shared frameworks conceal important differences. HairnThere uses a delivery exception; MailFlow uses NextAuth; KanjiForge has SQLite/OPFS locally and PostgreSQL remotely; other apps use MongoDB. A PWA manifest does not establish offline writes, and a `ci` script does not establish a reliable merge gate. Read the actual contract in the target brief and current source. [HairnThere](../../projects/briefs/hair-n-there.md), [MailFlow](../../projects/briefs/mail-flow.md), [KanjiForge](../../projects/briefs/kanji-forge.md).

**Distinguish authority from descriptions of state.** HairnThere's standing delivery instruction remains applicable even though its product-state assertions have drifted. Blockparty's source selects classic content while older AGENTS prose still describes placeholder activation as future work. A stale descriptive sentence should trigger source/decision review; it does not invalidate unrelated operating policy. [HairnThere](../../projects/briefs/hair-n-there.md), [Blockparty](../../projects/briefs/blockparty.md).

**Name what success actually acknowledges.** HairnThere requires a Discord response with a message ID before acknowledging an inquiry; Flowers acknowledges the database write even when optional notifications fail. MailFlow can complete an external Gmail effect before later progress/log writes fail. Each needs its own retry and recovery reasoning. None of these source traces establishes deployed delivery health. [HairnThere](../../projects/briefs/hair-n-there.md), [Flowers](../../projects/briefs/flowers.md), [MailFlow](../../projects/briefs/mail-flow.md).

**Inspect the complete persistence path.** Local SQLite commit, OPFS export, outbox enqueue, server acknowledgement, and replay are different events. KanjiForge's source exposes several seams requiring end-to-end verification. A recovery plan should state exactly what a backup includes and whether restoring it propagates to other devices. [KanjiForge](../../projects/briefs/kanji-forge.md).

**Keep personal context scoped and attributable.** Ants is a planning project whose handoff mixes confirmed decisions with proposals; its business model is not global policy. Lighthouse belongs to another person's continuity records and supplies its own governance. Shared skill procedures can carry side effects and invocation-specific gates; reading one does not grant authority to execute it. [Ants](../../projects/briefs/ants.md), [Lighthouse](../../projects/briefs/lighthouse.md), [agent-skills](../../projects/briefs/agent-skills.md).

**Treat available-on-disk and recoverable-from-Git separately.** Much of the current skills collection is local-only; Ants has uncommitted decision additions; Jarvis has no initial commit. These are evidence and backup concerns, not reasons to run a bulk commit/push operation. [agent-skills](../../projects/briefs/agent-skills.md), [Ants](../../projects/briefs/ants.md), [Jarvis](../../projects/briefs/jarvis.md).

## Source-derived follow-up candidates

These are candidates for separately scoped work, not a new implementation queue or permission to change applications. Reconfirm the current source before acting. A static concern is not a reproduced incident, an exploit report, or evidence about production data.

| Project | Candidate | What remains to establish |
| --- | --- | --- |
| HairnThere | Reconcile product-state documentation for public prices, closed appointments, and phone/email collection | Which documents should be updated to reflect the current recorded decisions |
| Flowers | Review CI exit propagation/lint and notification acknowledgement/consent-instruction boundaries | Intended operator workflow and a focused regression check |
| Grub Roulette | Photo URLs include the Google API key despite server-only guidance | Approved photo-delivery design and actual provider restrictions; no live credential was inspected |
| Blockparty | Reclaim approval appears to set the returned seat capability on the approving host response | A two-device reclaim test and the intended return-device exchange |
| KanjiForge | Study payload/server validation, outbox wake-up, and replay/backup projection continuity | Behavior across a real authenticated write/read/reconnect sequence |
| MailFlow | External action versus cursor/log idempotency; reply-log retention after disconnect | Intended retry, deletion/retention, and multi-device contracts |
| agent-skills | Untracked procedures, staged deletions, missing references, and unpinned distribution provenance | Which local changes Harry wants shared and the authoritative upstream/update route |
| Lighthouse | Conflicting confidence scales, navigation drift, and unspecified technical restore | Owner-approved governance reconciliation and a tested recovery procedure |
| PantryIQ | Fallback CSV identities, naive timestamps, and invalidation paths have different guarantees | Import identity/timezone contracts and reconciliation-to-recompute behavior |
| Platter | Completion revision and membership-revocation boundaries need verification; CI covers less than documentation claims | Concurrent mutation/completion and revocation tests, intended required gates |
| Scaffold | Public settings placeholder, stale index database names, and startup/lint configuration drift | Correct project-specific initialization before reuse |
| Portfolio | Shared CRM ingress validation/authorization and distinct app registries | Actual consumer contracts, consent and index provisioning |
| Tokei | Detail/update ownership and tick-based timer lifecycle | Tenant checks and real device/background behavior |
| VoiceBridge | Broad permissions/self-enrollment and ownership fields; incomplete editing/cache paths | Intended role model and focused authorization/UI consistency checks |
| Utility Scripts | Unguarded directory changes, broad commits, inherited push targets | A separately scoped maintenance workflow; scripts remain unexecuted |
| Wiki | Draft space metadata exposure, nested README root assumptions, and non-failing broken links | Publication/access intent and a focused content-index/link validation contract |

Route Roulette's directions depend on name-based external Maps resolution and distance-sorted discovery, with randomness added in the browser. Rise Above Drone is a YouTube showcase without the assumed lead/CRM flow; its brief distinguishes stale local tooling guidance from newer remote guidance. The prompts collection supplies reusable documents, not a runnable scheduler. These observations correct assumptions without creating new feature work.

Detailed findings stay in their project briefs. This synthesis should remain small and be revised when a follow-up resolves or supersedes an observation.
