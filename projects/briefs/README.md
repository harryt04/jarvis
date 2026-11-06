# Source learning pass

Harry requested a dedicated subagent investigation of every project on 2026-11-06, with HairnThere first and all others equally prioritized. Reviews run in bounded parallel batches. Each investigator writes only its assigned Jarvis brief; the source repositories remain read-only.

All 23 account repositories now have parent-reviewed source briefs linked below. An inventory entry is not a claim that the source has been learned. Each brief records its source revision, local-change caveats, evidence, and verification limits.

## Completion criteria

- Every account repository has a brief, including explicit remote-only or conceptual coverage where appropriate.
- Application briefs trace real user/data flows; knowledge/tooling briefs trace actual document/procedure ownership.
- Claims distinguish source implementation, documented intent, inference, and unknowns.
- Source paths/lines support the useful invariants and gotchas. No credentials, customer records, or employer internals are imported.
- Commands are inspected, not represented as passing checks unless executed separately under an appropriate task.
- The parent reviews each brief, adds it to the registry, and checks coverage and document links.

Lighthouse coverage is limited to its operating structure and privacy/record-integrity rules, not Elisabeth's personal records. Ants coverage excludes employer-derived source notes. MiniZinc Web may require read-only GitHub source inspection because no local checkout was found.

## Coverage

| Repository | Status | Brief |
| --- | --- | --- |
| harryt04/hair-n-there | Source brief reviewed | [hair-n-there](hair-n-there.md) |
| harryt04/agent-skills | Source brief reviewed | [agent-skills](agent-skills.md) |
| harryt04/ants | Source brief reviewed | [ants](ants.md) |
| harryt04/blockparty | Source brief reviewed | [blockparty](blockparty.md) |
| harryt04/flowers | Source brief reviewed | [flowers](flowers.md) |
| harryt04/grub-roulette | Source brief reviewed | [grub-roulette](grub-roulette.md) |
| harryt04/jarvis | Source brief reviewed | [jarvis](jarvis.md) |
| harryt04/kanji-forge | Source brief reviewed | [kanji-forge](kanji-forge.md) |
| harryt04/lighthouse | Source brief reviewed | [lighthouse](lighthouse.md) |
| harryt04/mail-flow | Source brief reviewed | [mail-flow](mail-flow.md) |
| harryt04/minizinc-web | Source brief reviewed | [minizinc-web](minizinc-web.md) |
| harryt04/pantry-iq | Source brief reviewed | [pantry-iq](pantry-iq.md) |
| harryt04/personal-project-scaffolding | Source brief reviewed | [personal-project-scaffolding](personal-project-scaffolding.md) |
| harryt04/platter | Source brief reviewed | [platter](platter.md) |
| harryt04/portfolio | Source brief reviewed | [portfolio](portfolio.md) |
| harryt04/prompts | Source brief reviewed | [prompts](prompts.md) |
| harryt04/rise-above-drone | Source brief reviewed | [rise-above-drone](rise-above-drone.md) |
| harryt04/route-roulette | Source brief reviewed | [route-roulette](route-roulette.md) |
| harryt04/ski-auto-parking | Source brief reviewed | [ski-auto-parking](ski-auto-parking.md) |
| harryt04/tokei | Source brief reviewed | [tokei](tokei.md) |
| harryt04/utility-scripts | Source brief reviewed | [utility-scripts](utility-scripts.md) |
| harryt04/voice-bridge | Source brief reviewed | [voice-bridge](voice-bridge.md) |
| harryt04/wiki | Source brief reviewed | [wiki](wiki.md) |

See [cross-project findings](../../docs/research/portfolio-findings.md) for the small synthesis and follow-up candidates. All reviews were static. MiniZinc used remote source; Lighthouse coverage was limited to governance; some briefs identify working-tree evidence or newer remote guidance explicitly. Runtime and production claims remain unverified.

## Final verification

Coverage matches all 23 registry entries. Local document links, registry consistency, authored-file whitespace, and obvious credential patterns were checked. One Platter source anchor was corrected; the longer drone README anchor was checked against its cited newer remote revision. Source HEADs, porcelain status, and tracked-diff hashes match the pre-review baseline across the inspected local source checkouts. These checks do not validate every semantic claim or deployed behavior. Harry subsequently authorized the initial commit and push to `main`; the earlier discovery snapshots describe the pre-publication state. No startup adapter or synchronization was installed.
