# Lighthouse audit worker prompt

`scripts/render_prompts.py` fills the `{{...}}` fields below and emits one copy
per repository. Edit this template, not rendered copies.

<!-- BEGIN TEMPLATE -->
Lighthouse audit for **{{NAME}}** (`{{REPO_ID}}`)

You are running in the Jarvis project; the target is a sibling checkout. Do the
work yourself; start no subagents or new threads.

1. **Refresh Jarvis.** Follow Jarvis `AGENTS.md` startup: safely refresh from
   `origin/main`, read README, `context/` files, and
   `docs/treehouse-workflow.md`. Resolve `{{REPO_ID}}` in
   `projects/catalog.json` and read `projects/{{BRIEF}}`. Do not edit Jarvis in
   this task; put any portable lesson in your final report instead.
2. **Verify the target.** Expected checkout: `../{{FOLDER}}` (from the Jarvis
   primary checkout). Confirm its `origin` is `{{REPO_ID}}`; if it is missing or
   differs, stop and report. Read its `AGENTS.md`/`CLAUDE.md`, README, and
   `package.json`. Discover the default branch
   (`git symbolic-ref refs/remotes/origin/HEAD`) and `git fetch origin`. Leave
   the primary checkout's branch and changes untouched.
3. **Applicability.** If the repo has no browser-rendered web UI, stop: report
   "not applicable" with evidence and open no PR.
4. **Worktree.** From the target checkout, run
   `treehouse get --lease --json --base <default> -b perf/lighthouse-audit-{{DATE}}`
   (reuse an existing lease for that branch if one exists). Verify worktree
   `HEAD` equals `origin/<default>` before doing anything else. Do all installs,
   builds, edits, and commits in that worktree path.
5. **Serve a production build.** Install with the repo's lockfile package
   manager and build/start the production server (for example `next build` then
   `next start -p <free port>`); dev servers distort performance scores. Use
   documented local/e2e/test configuration and `.env.example` values only. Never
   copy production secrets. If the build cannot run without unavailable
   configuration, record the blocker; as a read-only fallback you may audit the
   public deployment URL from the repo or brief, labelled as such.
6. **Audit.** Run `npm view lighthouse version`, then pin it:
   `npx --yes lighthouse@<version>`. It requires Node >= 22.19. Set `CHROME_PATH`
   to the installed Chrome or Chromium and pass
   `--chrome-flags="--headless=new"`. Add `--no-sandbox` only if Chrome
   refuses to start. Audit up to five representative public routes: home, plus
   the main conversion or content pages found in the router. Audit
   authenticated routes only when the repo documents a local test login. For each
   route, run the default mobile config and `--preset=desktop`, covering
   performance, accessibility, best-practices, and seo. Run performance three
   times and use the median. Save HTML and JSON reports outside the repo at
   `~/.jarvis/audits/lighthouse/{{SLUG}}/{{DATE}}/` with names
   `<route>-<mobile|desktop>-<run>.report.{html,json}`.
7. **Triage.** Fix findings that have a clear, attributable cause in this
   repo's code, such as:
   - missing alt text, labels, names, or `lang`
   - contrast failures in theme tokens
   - heading order
   - missing meta description, canonical, or `robots` and sitemap problems
   - unsized or unoptimized images, or LCP images without priority or preload
   - render-blocking fonts or scripts
   - avoidable client JS, such as heavy imports that could be lazy-loaded
   - console errors
   - deprecated APIs and insecure requests

   Skip lab noise and third-party-only costs, and record why. Also skip
   redesigns, major dependency upgrades, and changes that conflict with the
   repo's documented brand or design rules. Keep one coherent PR: accessibility
   and SEO fixes outrank micro performance tweaks. Do not add Lighthouse CI or
   new dependencies unless the repo already uses them.
8. **Verify.** Run the repo's real checks: lint, typecheck, tests, and build,
   as its instructions specify. Then re-run the same Lighthouse matrix against
   the rebuilt app. Stop every server and Chrome process you started.
9. **Deliver.** If you changed code, commit, push the branch, and open a PR
   against `<default>`. Do not commit the reports. The PR body should include:
   - a before/after score table (route × form factor × category, medians)
   - the fixes, each with the audit ID that motivated it
   - the findings you skipped, with reasons
   - the Lighthouse version, Chrome version, and whether you audited local
     production or the public URL
   - which checks you ran, with results

   If nothing worth changing was found, open no PR; report the scores and why.
   Do not merge, deploy, or clean up the worktree. If T3 PR tools are available,
   link the PR.
10. **Report.** Summarize the scores, the changes, the skipped findings, the
   blockers, and the report folder. End with exactly one line:
   `PR <full URL>, head <SHA>, checks <state>` or
   `No PR: <reason>`.
<!-- END TEMPLATE -->
