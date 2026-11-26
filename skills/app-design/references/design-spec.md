# The design spec

One self-contained HTML file that is both the thing Harry reviews and the
target builders validate against. It opens by double-click: no build step, no
server, no local assets. It lives in the project at
`docs/design/<name>-design.html`.

## Start from the template

Copy [../assets/design-spec-template.html](../assets/design-spec-template.html).
It already contains:

- The token block, under shadcn variable names, for three themes in light and
  dark, switched by `data-theme` and `data-mode` on `<html>`, with the theme
  and mode switchers wired up.
- shadcn-style primitives as plain CSS: `.btn` (`.out`, `.gh`, `.acc`, `.sm`,
  `.lg`, `.ic`), `.card`, `.inp`, `.lbl`, `.hint`, `.badge` (`.ok`, `.warn`,
  `.off`), `.sw` (switch), `.tabs`, `.chip`, `.sep`, tables (`.tw` > `table.t`).
- Browser and phone frames (`.frame`, `.phone`), a host-page backdrop
  (`.host`) for showing an embedded component, and the signed-in shell
  (`.shell` with `data-shell="<active nav label>"`; a script injects the
  sidebar from the `NAV`, `WORKSPACE` and `USER` constants).
- An icon sprite (`<svg class="i"><use href="#check"/></svg>`): `cal`,
  `clock`, `list`, `tag`, `code`, `gear`, `check`, `x`, `plus`, `cl`, `cr`,
  `ud`, `copy`, `warn`, `globe`, `sync`. Add lucide paths as needed.
- Screen blocks with ID pills and `.checks` lists, and decision forms that
  queue an answer to Lavish.

Replace the three palettes with new candidates (see `ui-preferences.md`),
replace every placeholder, and delete what the app does not need.

## Sections, in order

1. **Hero.** A one-line promise, two or three sentences, and a note that this
   page is the build target.
2. **Shape of the product.** A hand-drawn inline SVG diagram of the actors and
   systems with labelled arrows, using token colors so it follows the theme.
   Then a table defining every domain noun the screens use, each with an
   example. This table prevents builders inventing their own vocabulary.
3. **Look and color.** Swatches, categorical colors, the status examples, and
   the global checks `T-1` to `T-6`.
4. **Screens.** Every v1 screen. Group by audience when there is more than one
   (signed-in, public, embedded).
5. **Components**, if the app ships any to other projects: shown inside a
   pretend host page, with a table of exports and props.
6. **Build plan.** Stack table with adjustments, cards explaining the hard
   problems in plain language, what is not in v1, the slices with builder and
   reviewer, and the one operational trap to design around.
7. **Decisions.** Open questions as forms, each with a recommended option.

## Screens

- Give each an ID: `S1`, `S2`… for screens, `C1`… for shipped components.
  IDs never get reused or renumbered once Harry has seen them.
- Show the route beside the title.
- Signed-in screens sit in a browser frame with the shell. Public screens have
  no sidebar. Anything a customer uses also gets a phone frame.
- Fill them with realistic content for one believable example business, the
  same one throughout.
- Cover the whole v1: sign-in, the home screen, each management screen, each
  editor, settings that matter, the public flow, the "manage my thing" page,
  and any developer or integration screen.
- Draw at least one failure state and one attention state.
- **Make the single most important flow clickable** with a small state machine
  in vanilla JS (in OpenSlots: choose service, day, time, enter details,
  confirmation, driven by a fake availability function). Its behaviour is the
  reference for builders, so make the rules real, not random.
- Keep horizontal overflow contained: desktop mock bodies get a `min-width`
  inside a scrolling frame; grid and flex children need `min-width: 0`.

## Acceptance checks

Under each screen, three to six checks with IDs like `S4-2`. A good check is
something a builder can confirm by looking or clicking, and it captures a
decision that the picture alone does not make obvious:

- Behaviour: "‘Start times every’ is independent of duration, so a 180 min
  service can start hourly."
- Failure: "If the slot was taken while the form was open, the customer
  returns to the time step with a plain message."
- Constraint: "Exactly one calendar per business receives new bookings."
- Privacy or safety: "Only free/busy times are read; event titles are never
  fetched or stored."

Avoid checks that restate the picture ("there is a button") or cannot be
verified ("feels fast").

The global checks, every time:

| ID | Rule |
| --- | --- |
| T-1 | Colors come from the CSS variables only. No raw hex in components. |
| T-2 | shadcn/ui components only, built on UI SDK behaviors (no Radix UI or Base UI primitives). Tailwind v4, new-york style. |
| T-3 | Geist for UI. Geist Mono for times, durations, keys and code. |
| T-4 | Text contrast meets WCAG AA in light and dark. |
| T-5 | Any state shown with color also has an icon, label or text decoration. No red versus green. |
| T-6 | Visible 2px focus ring on every interactive element. |

## Decisions

Use real forms: radio options, a "Recommended" tag, one **Queue answer**
button per question that calls `window.lavish.queuePrompt` once. Always
include the theme question. Add only questions whose answer changes scope or
structure, each with plain-language cost ("adds roughly a third more work").
Three or four questions at most.

## Check it before he sees it

Render headless and read the screenshots yourself:

```sh
chromium --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1300,9000 --virtual-time-budget=4000 \
  --screenshot=full.png file:///abs/path/<name>-design.html
magick full.png -crop 1300x2250 +repage part-%d.png
```

Look for: text that wrapped badly, flex rows that split a sentence into
columns, anything unreadable on its fill, empty frames, broken scripts. Check
dark mode and at least one alternate theme the same way (set `data-mode` and
`data-theme` on `<html>` temporarily, or script the click), and the phone
width for public screens. Tell Harry which of these you did not check.

For live interaction checks, use the `agent-browser` skill.

## Review

Follow the `lavish` skill; get its current guidance from the CLI. Design
source to state when you deliver: the user asked for a specific look (Vercel
structure, shadcn, punchy colorblind-safe color), so the spec is hand-styled
to match that, not Lavish's default kit.

## After approval

- Replace the decision forms with a table: decision, what was adopted, the
  alternative left for later. Remove the forms' script.
- Make the adopted theme the default `data-theme`. Keep the other two in the
  token block as alternates.
- Replace personal names in roles with "maintainer" if the repository is
  public.
- Write `docs/design/README.md`: how to use the spec, how to validate a screen
  against it, the `T-*` table, and the sentence that the maintainer is
  colorblind so `T-5` is a hard requirement.
- Expect the build to add `docs/design/CHECKS.md` recording each check as met,
  met with a difference, not met, or not verified. Ask for it in the
  orchestration plan's final slice.
