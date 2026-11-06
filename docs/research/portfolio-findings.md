# Portfolio learning: cross-project findings

Observed 2026-11-06. This is the parent synthesis of reviewed [source briefs](../../projects/briefs/README.md). It records navigation lessons and follow-up candidates from static investigation. No application builds, tests, services, accounts, or deployed behavior were exercised. The briefs carry the revision-pinned evidence and project-specific detail.

All 23 repositories received an independent brief. HairnThere started first; the remaining projects had equal priority. Investigations begun after Harry's model-setting correction used GPT-6.1 Sol at medium reasoning. MiniZinc was inspected through authenticated GitHub source APIs; Lighthouse was reviewed for operating structure only. Source revisions and scope limits belong to each brief, not a claim of exhaustive or live production expertise.

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
| MiniZinc Web | Archived native solver boundary lacks apparent per-user authorization/job isolation; historical credential paths exist | Whether revival is wanted, then a fresh controlled review; credential validity was not inspected |
| PantryIQ | Fallback CSV identities, naive timestamps, and invalidation paths have different guarantees | Import identity/timezone contracts and reconciliation-to-recompute behavior |
| Platter | Completion revision and membership-revocation boundaries need verification; CI covers less than documentation claims | Concurrent mutation/completion and revocation tests, intended required gates |
| Scaffold | Public settings placeholder, stale index database names, and startup/lint configuration drift | Correct project-specific initialization before reuse |
| Portfolio | Shared CRM ingress validation/authorization and distinct app registries | Actual consumer contracts, consent and index provisioning |
| Parking bot | Plaintext credentials, date/resort routing mismatch, heuristic booking confirmation | Credential handling and a controlled non-booking verification plan before use |
| Tokei | Detail/update ownership and tick-based timer lifecycle | Tenant checks and real device/background behavior |
| VoiceBridge | Broad permissions/self-enrollment and ownership fields; incomplete editing/cache paths | Intended role model and focused authorization/UI consistency checks |
| Utility Scripts | Unguarded directory changes, broad commits, inherited push targets | A separately scoped maintenance workflow; scripts remain unexecuted |
| Wiki | Draft space metadata exposure, nested README root assumptions, and non-failing broken links | Publication/access intent and a focused content-index/link validation contract |

Route Roulette's directions depend on name-based external Maps resolution and distance-sorted discovery, with randomness added in the browser. Rise Above Drone is a YouTube showcase without the assumed lead/CRM flow; its brief distinguishes stale local tooling guidance from newer remote guidance. The prompts collection supplies reusable documents, not a runnable scheduler. These observations correct assumptions without creating new feature work.

Detailed findings stay in their project briefs. This synthesis should remain small and be revised when a follow-up resolves or supersedes an observation.
