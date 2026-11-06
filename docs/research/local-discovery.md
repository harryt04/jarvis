# Local discovery evidence

Observed: 2026-11-06. Read-only inspection of sibling repositories, Git metadata, selected source/manifests, current agent guidance, the supplied global worktree workflow, the public GitHub user profile, and authenticated `gh repo list harryt04 --limit 200`. No email/calendar/Linear exploration, application execution, provider session archive mining, or production access was needed.

## Coverage

The account query returned **23 repositories**, including private and archived entries; none was marked as a fork. [The registry](../../projects/catalog.json) accounts for every result. Twenty-two have a local candidate checkout when including Jarvis, the external `~/.agents/skills` checkout, and the provisional Ants association. `minizinc-web` was not found locally and received metadata-only coverage. Several repos received guidance/manifest review rather than a line-by-line source audit.

Initial GitHub metadata says Jarvis is private and has no default branch. The local Jarvis checkout is on unborn `master`, has no commits or configured origin, and initially contained only an empty untracked `.gitignore`. No worktree was created/acquired, no branch was changed, and no commit, push, or PR was performed for this planning pass. The supplied worktree workflow was read; its PR default and explicit exceptions are recorded in the plan.

Multiple target checkouts already had local changes. They were left untouched. Per-project source HEADs and changed-path counts are recorded in the registry; a HEAD identifies the baseline, not a guarantee that every observed local file matches that commit. Source pointers must be rechecked when a task starts.

## Identity and path traps

- `hair` is `harryt04/hair-n-there`; `autopark` is `harryt04/ski-auto-parking`; `scaffolding` is `harryt04/personal-project-scaffolding`; `voicebridge` is `harryt04/voice-bridge`.
- `wiki` has an old `harryt04/markdown-webserver` origin; GitHub's repository API resolves it to `harryt04/wiki`.
- `rise-above-drone` has an old `harryt04/hizzy-drone` origin; GitHub's repository API resolves it to `harryt04/rise-above-drone`.
- `ants` has local history and planning files but no origin. Its account repository has no default branch in the API response. The association is provisional, not verified by a matching remote.
- `agent-skills` is checked out at `~/.agents/skills`, with matching origin. It is an existing cross-machine capability source.
- Extra `kanji-forge-*` directories are additional checkouts/worktrees of one repository. `firstmate` and `rs-sdk` have other owners. An `emails` directory was not explored.

## Reusable findings

1. **Specifications already carry valuable context.** KanjiForge, PantryIQ, Blockparty, MailFlow, VoiceBridge, and Platter have substantial documentation. Jarvis should index it rather than fork it.
2. **The scaffold is a preference, not universal architecture.** PantryIQ and KanjiForge use PostgreSQL/Drizzle. MailFlow uses NextAuth. Route Roulette uses Material UI. Some newer shadcn presets use Base UI rather than Radix APIs.
3. **Current-state claims can conflict.** Blockparty's root AGENTS says its classic bundle remains to land, while its README says activation has happened. This is a reason to inspect source and the authoritative docs before claiming status, not to choose whichever sentence sounds newer.
4. **A check named CI is not automatically a reliable gate.** Flowers currently has `prettier --write .; npm run build; npm run test`; it mutates files, omits lint, and reports the final command's result even if the build fails. This is an observed shell-script hazard, not a runtime test result. Several other projects retain `next lint` scripts whose compatibility needs checking against their installed framework version. Do not run bulk auto-fixes while doing discovery.
5. **Some old automation embodies the old workflow.** `utility-scripts/update-packages.sh` commits/pushes across projects and refers to absent legacy PantryIQ directories. It should not be run as the new hygiene rollout.
6. **Knowledge boundaries matter.** Lighthouse describes Elisabeth's sensitive private continuity records. Only its purpose and access boundary were captured. The wiki publishes its `content/` tree, so connecting it to Jarvis memory would risk exposing private context.
7. **Prior preferences need provenance.** The Ants handoff contains useful attributed preferences, but it is a prior agent summary. Those are labeled historical in the Harry profile. Employer-derived planning notes were not copied into this repository.

## Verification limits

No application builds, tests, migrations, bookings, notifications, or inbox actions were run. Configured portfolio URLs were read as project metadata, not checked for availability. Package scripts and workflow files were inspected, not certified green. Credentials and environment-file values were not collected. No global agent configuration or machine directory was modified.

This pass provides a navigable starting inventory and an implementable plan. Becoming a reliable expert on each codebase requires targeted source investigation and feedback during real work.
