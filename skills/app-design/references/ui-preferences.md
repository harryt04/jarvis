# Harry's UI and UX preferences

Sources are marked. **Confirmed** means Harry said it. **Observed** means he
reacted to it. **Interpretation** is an agent's reading and can be wrong;
prefer his current words over anything here.

## What he asked for

Confirmed, OpenSlots design session, 2026-11-16:

- "This application should look like Vercel designed it, and use shadcn UI
  components."
- "Pick a color theme that is random or unique."
- "I am colorblind and love punchy colors rather than monochromatic and black
  and white themes everywhere."
- He wants mockups before the build "so implementation agents will have
  something to validate their work against."

Observed, same session: shown a spec built on the rules below, with the
Voltage theme (electric violet primary, tangerine accent on a faintly tinted
background), he wrote "oh my god this looks gorgeous." He did not choose
between the three candidate themes; Voltage was adopted as the recommended
default. Treat the overall approach as validated and the specific hue as one
example, not a house color.

Unknown: which kind of color vision deficiency he has. Do not guess in
documents. If a design decision hinges on it, ask him once.

## Landing pages

Sky Survey landing session, 2026-11-17:

- **Confirmed:** "it should look like the website/webapp was designed by UI UX
  experts at Vercel", shadcn components wherever possible, and "come up with
  3-5 ideas and get my feedback in lavish". He named his inspiration sites:
  repostaff.com ("which I recently made and very proud of"), omarchy.org and
  swamp-club.com. All three are dark, mono-labelled, numbered-section pages
  with one bold brand moment.
- **Observed:** shown five live concepts (a dark drone-viewfinder hero, a
  light timeline scrubber, a pixel tile-mapping animation, a product-led
  clickable client app, a scroll-driven swipe), he picked the product-led one
  ("I like option D the most") and asked for the full page. Then: "this looks
  great let's build this". The dark, HUD-style options closest to his
  references were not chosen.
- **Interpretation:** his references set the energy (confident type,
  numbered sections, interactivity), not the literal look. What won was the
  real product, clickable, in the hero, with a walkthrough of one concrete
  example (a week's delivery from flight to client). Lead with that kind of
  concept next time, and still offer bolder ones.
- **Copy, observed:** he replaced "Ship the week." with "Ship weekly maps.":
  he prefers concrete nouns over clever abstraction in headlines.
- **Process, confirmed:** when a Lavish review is waiting on him, the T3
  thread must show as waiting, not working (see "Waiting on Harry" in
  `AGENTS.md`).

## The look: Vercel structure, real color

Interpretation of "like Vercel designed it", validated by his reaction:

- **Type:** Geist for interface text, Geist Mono for anything precise (times,
  durations, IDs, keys, code). Tight negative letter spacing on headings.
- **Structure:** hairline 1px borders, 8 to 12px radii, restrained shadows,
  generous white space, dense but calm tables and lists.
- **Hierarchy by size and weight.** The most important number on a card is the
  biggest thing on it.
- **Chrome:** a sidebar shell for signed-in apps with a workspace switcher at
  the top (he runs several businesses), the user at the bottom, and a
  needs-attention icon on any nav item that has a problem.
- **Copy:** plain, short, specific. Every screen has one sentence under its
  title saying what it is for. Helper text explains consequences.

Where it departs from Vercel, on purpose: Vercel is black and white. He
dislikes that. Keep the structure and put color to work:

- The page background is faintly tinted toward the primary, never pure white
  or pure black. Sidebar and muted surfaces carry a slightly stronger tint.
- Primary color on actions, the active nav item and selected states.
- A second, contrasting punchy color for the single most important thing on a
  screen (the chosen item, the key call to action, the metric that matters).
- A soft tint of the primary for hover and "available" states.
- Gradients sparingly, on brand moments: the sign-in panel, a hero, an avatar.
- Categorical data (services, tags, calendars) gets its own color and always
  its name beside it.

## Color rules that come from colorblindness

These are requirements, not polish. Put them in every spec as checks `T-4` and
`T-5`, and in the project's `AGENTS.md`.

1. **Never carry meaning by color alone.** Every state has an icon, a word, or
   a text decoration as well: a check beside "Confirmed", a warning triangle
   beside "Needs reconnect", strike-through on cancelled or unavailable items.
2. **No red versus green**, anywhere. Not for success and error, not for
   charts, not for diffs.
3. **Pair a cool primary with a warm accent** (or the reverse). Blue or violet
   against orange or yellow stays distinct under the common red-green
   deficiencies. Avoid pairing colors that differ mainly in red-green content
   (red/green, green/brown, blue/purple, pink/grey).
4. **Categorical colors come from the Okabe-Ito palette**, which is designed
   for color vision deficiency: `#0072B2`, `#E69F00`, `#56B4E9`, `#D55E00`,
   `#CC79A7`, `#F0E442`, `#009E73`. Use it as-is for chips, bars and dots.
5. **Destructive and error states** use a vermillion or deep orange with a
   warning icon and bold text, not a pure red that can read as dark grey.
6. **Contrast meets WCAG AA** in light and dark. Put dark text on orange,
   yellow and other light, saturated fills; white text fails there.
7. **Differences in lightness do the heavy lifting.** Two states should still
   be tellable apart in a greyscale screenshot.

## Building theme candidates

Each new app gets its own theme. "Random or unique" is a real instruction:
do not reuse a theme from the table below, and do not default to the same hue
family every time.

- Offer **three candidates** on a live switcher in the spec, each with light
  and dark values, and a recommended one. He chooses by eye.
- Give each a short, memorable name ("Voltage", "Tidepool", "Flamingo").
- Each candidate defines the full shadcn token set plus `primary-soft`,
  `accent-strong`, `accent-strong-foreground`, `accent-strong-soft`,
  `highlight` and `sidebar`.
- In dark mode, lighten the primary and use dark text on it; tint the
  background toward the primary instead of using black.
- Let the product suggest the palette (a booking tool, a recipe app and a
  developer tool should not look alike), but keep rule 3.

### Token naming: avoid the `accent` collision

shadcn/ui components use the `accent` utility for quiet hover and highlight
surfaces (ghost buttons, menu items, calendar cells). The OpenSlots spec used
`--accent` for its punchy tangerine, and the build had to remap it
(`bg-accent-strong`) and document the trap. Name it correctly from the start:

- `--accent` / `--accent-foreground`: the quiet hover surface, set to the
  primary-soft tint. This is what shadcn expects.
- `--accent-strong` / `--accent-strong-foreground` / `--accent-strong-soft`:
  the punchy second color.

The template already does this.

### Themes in use

Add a row when a project adopts a theme, so the next app looks different.

| Project | Theme | Primary | Strong accent | Adopted |
| --- | --- | --- | --- | --- |
| OpenSlots | Voltage | electric violet `#5B34F5` | tangerine `#FF6A13` | 2026-11-16 |
| Sky Survey | Hi-Vis | blueprint blue `#2B3BF0` | safety yellow `#F5E000` | 2026-11-17 |

Offered and not chosen (free to offer again): Tidepool (cobalt `#0A5CFF` with
amber `#FFB000`), Flamingo (magenta `#D1006C` with cyan `#00B8D9`), Updraft
(teal `#00727F` with orange `#FF9F1C`), Ember (burnt orange `#C43D08` with
cyan `#12B5D6`).

## Components

- shadcn/ui primitives only, added with its CLI, new-york style. No second UI
  kit. Mockups imitate them; the build uses the real ones.
- One status component per app that pairs every state with its icon, so nobody
  adds a color-only badge later.
- Form errors need an icon and a thicker border on the field. shadcn's
  `FormMessage` is colored text only; plan the fix in the spec's token checks.
- Light and dark from the first commit, following the system by default.
- Visible 2px focus ring on every interactive element; full keyboard use.

## UX habits that have worked for him

Observed in the OpenSlots spec he approved:

- **Show the consequence.** A live preview beside a settings form (what this
  rule does to Wednesday) beats a paragraph of explanation.
- **Realistic sample data.** Real-sounding names, plausible times, a believable
  business. Never lorem ipsum, never "Item 1".
- **Design the bad day.** Each spec includes at least one failure state drawn
  out (a broken connection, a taken slot, an empty list) and says what the
  user sees.
- **Fail closed, and say why.** When the app cannot be sure, it stops and
  explains, instead of guessing.
- **Phone first for anything a customer touches.** Layout responds to the
  component's own width, so it also works embedded in a narrow column.
- **No account for the public.** People who only consume (customers, guests)
  should not have to sign up.
- **One screen, one job**, with the primary action top right.
- **Empty states point somewhere.**

## Recurring product leanings

From `context/harry.md` (working inferences there, not mandates): offline use,
accessibility, user-owned data and understandable behavior recur across his
projects. Self-hosting and open source came up strongly for OpenSlots ("There
should be a FOSS self-hosted option"). Ask whether they apply; do not assume.
