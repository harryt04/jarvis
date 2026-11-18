---
name: app-design
description: Design a new application for Harry before any code is written - name it, shape v1, pick the architecture on his scaffold stack, and produce a clickable HTML design spec with screen IDs and acceptance checks, reviewed in Lavish, followed by PRD, TRD, an orchestration plan and a copy-paste kickoff prompt. Carries Harry's UI/UX taste (Vercel-style structure, shadcn/ui, punchy colorblind-safe themes, never monochrome) and his tech stack defaults. Use for /app-design, "design a new app", "I want to build X", "plan a new project", "help me build a plan for a repo", "mock up the screens", "make a PRD/TRD", "pick a name for this app", "design this the way I like", or any new product idea, even when Harry does not say "design" or "skill". Also use when adding a major new surface to an existing app of his and the look or architecture is undecided. Not for implementing an already-approved spec, small UI tweaks, or auditing an existing site (use lighthouse-audit).
---

# App design

Take a product idea from a paragraph to an approved, buildable plan: a name, a
scoped v1, an architecture on Harry's stack, and a visual design spec that
implementation agents can validate against. This skill ends when Harry has a
repository of planning documents and a prompt he can paste to start the build.
It does not build the app.

The method comes from the OpenSlots design session (2026-11-16), which Harry
called "gorgeous" and asked to have repeated. `harryt04/openslots` is the worked
example: read its `docs/design/openslots-design.html`, `docs/PRD.md`,
`docs/TRD.md` and `docs/ORCHESTRATION.md` when you want to see the finished
standard. Do not copy its content or its theme.

## Reference files

| File | Read it when |
| --- | --- |
| [references/ui-preferences.md](references/ui-preferences.md) | Before any visual decision. Harry's taste, the colorblind rules, how to build theme candidates, themes already used. |
| [references/stack-and-architecture.md](references/stack-and-architecture.md) | Before proposing any technology or structure. His defaults and when a deviation is justified. |
| [references/design-spec.md](references/design-spec.md) | Before writing the HTML spec. Its anatomy, the template, IDs, acceptance checks, how to verify it. |
| [references/documents.md](references/documents.md) | After the design is approved. What the PRD, TRD, orchestration plan, AGENTS.md and kickoff prompt contain. |

## How to work with Harry here

- He gives an idea in a few loose sentences and expects you to fill gaps with
  good defaults. Decide what you reasonably can, state it, and keep moving.
- Ask only what changes the design, one self-contained question at a time, in
  plain language, with a recommendation. Product-fit calls are his.
- Be honest once about prior art and tradeoffs, then respect his decision. In
  the OpenSlots session he rejected forking a large existing project ("tons of
  baggage") in favour of a small implementation of his own. Expect that
  preference; do not relitigate it.
- Put visual decisions in front of him visually. He picks themes by eye.
- Concise prose, no em dashes.

## Workflow

### 1. Ground yourself

Refresh Jarvis as its `AGENTS.md` requires, then read the scaffold **live**:
`~/Documents/git/scaffolding` (GitHub `harryt04/personal-project-scaffolding`),
specifically its `AGENTS.md`, `package.json`, `components.json` and
`app/globals.css`. The scaffold changes; the snapshot in
`references/stack-and-architecture.md` tells you what to expect, not what is
true today. Skim the registry for sibling projects that solve a similar
problem; reuse their proven patterns.

### 2. Shape the idea

Restate the product in one paragraph: who uses it, what they get, what v1
includes and what it leaves out. Name the audiences (who signs in, who never
does). Do a brief prior-art check so he hears about a free alternative from
you and not later. Surface the one or two genuinely hard problems early (in
OpenSlots: no double booking, and an OAuth setup trap), because they drive
both screens and architecture.

### 3. Name it, if it has no name

Offer three or four candidates with one line each on why. He likes names that
say what the thing is and fit open source convention ("OpenSlots"). Check npm
and GitHub for collisions before recommending; say what you did not check
(domains, trademarks). Recommend one.

### 4. Create the project folder

A sibling of Jarvis: `~/Documents/git/<name>`, with `git init -b main`. Add an
MIT `LICENSE` (copyright Harry Thomas) unless he says otherwise; he wants his
projects MIT. Write the MIT text out; do not copy another repo's license file.
Do not create a GitHub repository or push until he asks or says to kick off.

### 5. Decide the architecture

Follow [references/stack-and-architecture.md](references/stack-and-architecture.md).
The scaffold stack is the answer unless a requirement truly cannot be met on
it. First try to solve the hard problem **on** his stack. If you still believe
a deviation is needed, present it as an explicit decision with the reason, and
accept "no".

### 6. Write the design spec

Follow [references/design-spec.md](references/design-spec.md) and start from
[assets/design-spec-template.html](assets/design-spec-template.html). Save it
in the project at `docs/design/<name>-design.html`. It holds: the product's
shape, three new theme candidates on a live switcher with light and dark,
every v1 screen with an ID and acceptance checks, the most important flow made
clickable, the build plan, and the open decisions as forms.

Render it headless and look at the screenshots before showing him. A broken
mockup wastes his review.

### 7. Review in Lavish

Use the `lavish` skill: fetch its current CLI guidance, open the session, and
wait on the poll through a tracked background job. While it waits, the session
is waiting on Harry, not working: follow "Waiting on Harry" in Jarvis
`AGENTS.md` (in T3, do not register the poll with `t3_background_wait`). Give him the session URL
and a short summary of what is in it and what he needs to decide. Apply
feedback and repeat until he approves or ends the session. If he ends it
without answering a decision, adopt your recommended option and tell him
plainly that you did.

### 8. Write the documents

Follow [references/documents.md](references/documents.md). Replace the
decision forms in the spec with a table of adopted decisions, then write the
PRD, TRD, orchestration plan, `AGENTS.md` (with `CLAUDE.md` symlinked to it),
`README.md`, `docs/design/README.md` and `.gitignore`. Mark any library fact
you have not checked against current documentation as **Verify** and assign it
to a build slice.

### 9. Kick off

When he asks to kick off: check links and private data, commit, and push. An
empty new repository has no branch to open a pull request against, so its
first documents-only commit goes to `main`; say so. Everything after that is
worktrees and pull requests. Give him the copy-paste orchestration prompt in a
code block. State what only he can do (cloud consoles, npm scopes, secrets).

Finish by recording anything durable you learned about his taste: update
[references/ui-preferences.md](references/ui-preferences.md) (including the
"Themes in use" table) through a Jarvis pull request.

## What done looks like

- He has seen every v1 screen, in color, before a line of app code exists.
- Each screen has an ID and checks a builder can tick off by looking or clicking.
- The spec is usable by someone who cannot tell red from green.
- The stack is his stack, and every deviation is named with its reason.
- The documents let an agent with no memory of this conversation build it.
- You told him what you verified and what you did not.
