# Documents written after the design is approved

All in the new project, in plain language, self-contained enough that an agent
with no memory of the design conversation can build from them. The repository
owns these; Jarvis keeps only a registry entry and a brief.

```
LICENSE              MIT
README.md            what it is, status, links to the documents
AGENTS.md            standing rules for any agent; CLAUDE.md is a symlink to it
.gitignore
docs/PRD.md
docs/TRD.md
docs/ORCHESTRATION.md
docs/design/<name>-design.html
docs/design/README.md
```

Requirement IDs (`R1`…) live in the PRD, screen IDs (`S1`…) in the spec. The
TRD and orchestration plan refer to both.

## PRD

1. **Summary.** One paragraph.
2. **Why.** The problem, in his terms.
3. **Who it is for.** A table of people and what each needs.
4. **Scope of v1.** "In" as numbered requirements `R1`…, each a sentence or
   two. "Out" as a plain list.
5. **Decisions already made.** Name, license, theme, the answers from review,
   the stack in one line.
6. **Key journeys.** Numbered, including at least one failure journey.
7. **Success criteria.** Verifiable: all spec checks pass, the hard-problem
   test passes, a fresh clone comes up from the guide alone, the first real
   use works.
8. **Risks.** A table of risk and handling.

## TRD

1. **Stack.** Table. Note the scaffold as the starting point and each adjustment.
2. **Repository layout.** A tree with a line per directory; root scripts.
3. **Data model.** A table per collection: fields, indexes. State the
   no-transactions assumption and which index carries integrity.
4. **Core logic.** The pure function's signature, its rules in order, and the
   list of required tests.
5. **The critical write path.** Numbered steps including each rollback, and
   the concurrency test that proves it.
6. **Integrations.** Scopes and permissions, token handling, the provider
   interface and its fake, caching, failure behaviour, setup traps. **Verify**
   markers go here.
7. **API.** A table of method, path, purpose, notes. Auth, error shape,
   protections, and the tenant-isolation test.
8. **Published packages**, if any: exports, props, peer dependencies, styling
   and theming, how the app consumes them.
9. **Security and privacy.** Secrets, tokens, what a public key can do, what
   customer data is held, sign-in restriction, headers.
10. **Configuration.** Table of environment variables: required or not, purpose.
11. **Testing and CI.** What is tested at which level; the CI steps.
12. **Deployment.**
13. **Open technical questions.** Usually only the Verify items.

## Orchestration plan

For the agent that will coordinate the build.

- **Ground rules:** the model ceiling; one slice, one branch, one worktree,
  one pull request; never push to `main`; the reviewer is always from the
  other provider and is a fresh delegate given the diff and the brief, not the
  builder's summary; ask once at the start for merge authority and otherwise
  stack slices on unmerged branches; never publish, deploy or change
  repository settings without approval; report failures honestly; correct the
  TRD in the same pull request when a slice proves it wrong.
- **Models table.** Harry's stated limits for the OpenSlots build
  (2026-11-16) were Claude Opus 5.5 at medium and below, and GPT-6.1 Sol at
  medium and below; his standing subagent default in `context/harry.md` is
  GPT-6.1 Sol at medium. Use those unless he says otherwise for this project,
  confirm available models with the harness before naming them, and never
  substitute silently. A split that worked: Opus for core logic and component
  design, Sonnet for screens, Haiku for documentation, Sol for integrations,
  API and tests.
- **Slices table:** slice, work, design IDs, TRD sections, builder, reviewer.
  Slices sharing a number run in parallel. A usual shape:
  0 bootstrap (orchestrator, serial); 1 core logic, auth and integrations,
  app shell; 2 the management screens; 3 the public API and any package;
  4 public pages, dashboard, end-to-end and visual pass with a security
  review; 5 self-hosting, docs and release preparation.
- **What every builder brief contains:** the slice row verbatim, the files to
  read, the exact base branch, what is out of scope, the definition of done,
  and the required last line (pull request URL, head commit, state of checks).
- **Definition of done:** CI passes; tests at the level the TRD names; for UI,
  the builder opened the screen in a browser beside the spec and the pull
  request lists each check as met or not, with light and dark screenshots; no
  raw colors and no color-only states; documents updated; cross-provider
  review resolved.
- **Handback:** what was built, every check not met and why, the manual steps
  left for Harry, a suggested first real use.

Keep Harry's private workflow (Jarvis, Treehouse, local paths) out of this
file when the repository is public. It goes in the kickoff prompt.

## AGENTS.md for the new project

Short. A "Read first" list (PRD, TRD, spec and its README, orchestration
plan); the rule that code and documents must not silently disagree; the fixed
stack; the project's two or three load-bearing invariants (the integrity
index, the pure core, the single UI); a `## UI SDK` section (shadcn/ui look on
UI SDK behaviors, the agent bridge and its allow policy); colors from
tokens and the colorblind rule with its reason; `proxy.ts`; secrets; query
scoping; the pull request workflow; and a Commands section that says it will
be filled in by the bootstrap slice and that commands must not be invented.

## README.md

What it is in two sentences, a clear status line ("planning complete, build
not started; there is no runnable code yet"), what it will do, links to the
documents, the license.

## Kickoff prompt

Give it to Harry in a fenced code block in chat. About 30 lines:

- What is being built, the repository URL, the local checkout, the scaffold path.
- The files to read first, ending with the orchestration plan as "your plan".
- Follow the Jarvis workflow: Treehouse worktrees, pull requests, never `main`.
- Add the project to the Jarvis registry and write its brief, as a Jarvis pull request.
- Do slice 0 yourself, then run the slices as named.
- The allowed models and the reasoning ceiling; stop if one is unavailable.
- Every UI slice checked in a browser against the spec, light and dark.
- "I am colorblind: no color-only states, no red versus green."
- Ask once, now, about merge authority; until answered, leave pull requests
  open and stack dependent slices.
- Never without explicit approval: publish, deploy, change repository settings.
- The final report to give.

## Before committing

Check relative links, that no secret or private detail is in a public
repository, `git diff --cached --check`, and that the spec still renders.
