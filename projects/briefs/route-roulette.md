# Route Roulette — source research brief

Observed **2026-11-06**. Read-only local source: `harryt04/route-roulette`, origin `https://github.com/harryt04/route-roulette.git`, branch `master`, HEAD **61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb**. `git status --porcelain=v1 --untracked-files=all` was empty; cited tracked files match this revision. Ignored environment/generated artifacts exist and are outside that cleanliness claim; their contents were not inspected. No applicable source AGENTS.md was found in the repository or checked ancestor locations. This brief follows Jarvis’s project-review contract. No application, API, test, build, dependency installation, service, or deployment was executed; remote/deployed state was not checked.

## Purpose and current shape

A small public scenic-drive discovery app: visitors share browser location, choose a search radius and visible waypoint count, optionally shuffle/remove places, then open Google Maps. README calls it free and open source and names Vercel plus `rr.harryt.dev` ([README:1–13,42–65][readme]). There are no accounts, database, saved itineraries, embedded map, navigation engine, offline workflow, or payment integration in the inspected source. The tip jar and feedback form are outbound links ([footer:8–53][footer]). “Random scenic drive” is product intent; the initial result is deterministic distance ordering, and actual roads/directions are delegated externally.

## Location → server → candidates

`page.tsx` owns the responsive title/footer and renders `RoutePlanner`. The geolocation hook calls `navigator.geolocation.getCurrentPosition` once on mount, without explicit timeout/options, watch, or retry. Success retains latitude/longitude in React state; no manual-origin fallback exists. Only permission-denied gets a visible explanation: unsupported browser, unavailable position, and timeout become hook strings that the planner never renders. Plan stays disabled without location ([hook:4–40][hook]; [planner:25–115][planner]).

Planner defaults to 10 miles and three displayed waypoints. Plan sends latitude, longitude, and radius through Axios to same-origin `POST /api/getRoute`; count never reaches the server. The Next route reads JSON, obtains server-only `GOOGLE_MAPS_API_KEY`, converts miles using 1609.34, and calls Google Places Nearby Search with literal keyword `scenic+viewpoint|park|tourist+attraction`. It performs one request, without pagination or explicit timeout/retry. Keyword interpretation and live API availability were not validated ([client:3–19][client]; [api:5–43][api]).

The server copies Google results, sorts ascending by haversine distance from the starting location, and returns only name and coordinates. Sorting is straight-line distance, not travel distance or route optimization; there is no scenic quality score, deduplication, or road accessibility check. `slice(0)` imposes no application-side result cap ([sorting:11–55][sorting]; [api:28–36][api]).

## Trust, validation, and errors

The API has no authentication, authorization, rate limiting, or quota guard in source, so the server key boundary does not prevent callers from consuming its upstream allowance. JSON parsing occurs outside the catch. Validation checks truthiness only: valid zero latitude/longitude is rejected, while truthy strings, negative radii, and out-of-range coordinates are not meaningfully validated. Inputs use `Number(...)` without min/max/integer constraints. Google response status/schema is trusted; a response with `results: []` can appear successful irrespective of its API-level status, while absent/malformed results can throw into the generic 500 ([api:5–42][api]; [planner:65–84][planner]).

Client errors are logged and converted to `[]`, making network/server failures indistinguishable from “No waypoints found.” Loading has no `finally`; the early no-location return leaves it set, although disabled UI normally prevents that path. Server error logging includes the upstream error object: logs may contain request configuration and sensitive context. No persistent location write appears in application code, but location crosses the server and Google boundary, and production telemetry exists. The footer’s absolute “never stored anywhere” statement therefore cannot establish infrastructure/provider retention policy ([client:16–18][client]; [planner:34–53,160–164][planner]; [footer:50–53][footer]).

## Candidates → randomness → directions

The UI retains all candidates but displays `slice(0, numWaypoints)`. Removing a displayed index deletes it from the backing list, allowing a previously hidden candidate to appear. Shuffle rearranges that whole list with `sort(() => Math.random() - 0.5)`: this is biased, unseeded randomness, makes no new Google request, and can change membership of the visible subset. Negative/fractional/zero counts inherit JavaScript slice semantics rather than a product constraint ([planner:44–56,117–156][planner]).

Directions uses origin coordinates, the last visible name as destination, and preceding names as intermediate waypoints. Although candidate coordinates were returned, they are discarded here. Names are quoted but not URL-encoded, so ambiguous names and reserved characters can resolve incorrectly. No travel mode, loop back to origin, waypoint-limit handling, or route optimization is requested. An empty visible subset yields an empty href even while backing candidates keep the Directions control rendered ([client:37–52][client]).

## Material UI, theme, analytics

This is Material UI v5 with Emotion/AppRouterCacheProvider, Cards, Typography, fields, icons, and CssBaseline, rather than a utility-CSS component system. Light/dark themes share lime primary and cyan secondary colors; palette mode changes defaults. Theme initializes light, then loads localStorage or system preference. Later system changes overwrite even a saved manual choice. Toggle and responsive `isMobile` are localStorage writes, not location persistence; neither path handles storage failures, and mobile JSON parsing is unguarded. Global CSS hardcodes a whitesmoke background alongside CssBaseline, creating a possible dark-mode styling conflict; CSS’s 768px layout breakpoint also differs from MUI’s default `sm` query ([theme:5–51][theme]; [provider:12–55][provider]; [page:15–44][page]; [css:1–8,106–122][css]).

Layout mounts Vercel Analytics and SpeedInsights only in production. PostHog packages are dependencies but no source initialization/use was found. Metadata still describes choosing a restaurant, contradicting the scenic-drive interface ([layout:9–19,42–51][layout]; [manifest:12–26][manifest]). These are project observations, not evidence of Harry’s global preferences.

## Checks, delivery, reading map

Manifest commands are `npm run dev`, `build` (`next build`), `start`, `lint` (`next lint`), and mutating `prettify`. README requires PRs targeting `master` and a build check. No tracked CI/deployment workflow or test suite was found. Vercel is documented, not independently verified; hosted branch, domains, secrets, quota restrictions, and retention remain unknown. Next is declared `^14.2.33`; ESLint config is `14.2.2`, and TypeScript strict mode explicitly permits implicit any ([manifest:5–36][manifest]; [tsconfig:2–10][tsconfig]).

For location/error changes read hook → planner → client; for Google/quota/validation changes read API → sorting; for navigation/randomness read planner → URL constructor; for appearance/telemetry read layout → provider → theme/CSS. Re-review before changing Places endpoints, URL identity, waypoint constraints, telemetry/privacy claims, or deployment checks. README’s explicit build/master policy is the supported project-scoped decision; broader personal intent is unproven.

[readme]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/README.md#L1-L65
[planner]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/components/routePlanner.tsx#L25-L165
[hook]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/hooks/useGeolocation.ts#L4-L40
[api]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/api/getRoute/route.ts#L5-L43
[client]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/client-utils/getRoute.ts#L3-L52
[sorting]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/shared-utils/sorting.ts#L11-L55
[footer]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/components/footer.tsx#L8-L53
[theme]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/theme.ts#L5-L51
[provider]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/CustomThemeProvider.tsx#L12-L55
[page]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/page.tsx#L15-L56
[css]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/globals.css#L1-L122
[layout]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/src/app/layout.tsx#L9-L51
[manifest]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/package.json#L5-L36
[tsconfig]: https://github.com/harryt04/route-roulette/blob/61e5068ab7c8d7a7b7cfd33f96c8e13125a89dcb/tsconfig.json#L2-L10
