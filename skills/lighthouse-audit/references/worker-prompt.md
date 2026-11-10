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
9. **Deliver.** If you changed code, commit and push the branch, then open a
   PR against `<default>`. Use exactly this title, for the commit too:
   `chore(lighthouse): {{DATE}} audit fixes`. Every audit PR shares this title
   so they can be found with one search. Do not commit the reports.

   Label the PR `lighthouse-audit`. Create the label first if the repo lacks
   it:
   `gh label create lighthouse-audit --color F4B400 --description "Lighthouse audit skill" 2>/dev/null || true`,
   then pass `--label lighthouse-audit` to `gh pr create`. If labeling fails,
   still open the PR and report why. The label and the PR body are the only
   durable record of this audit's results, so Jarvis reads them back later.

   The PR body must include a `## Lighthouse results` section with:
   - a before/after table of medians, route × form factor × category, with
     the route path, form factor, and four category scores as `before → after`
   - each route's three performance scores per form factor, so the variance is
     visible
   - the Lighthouse version, Chrome version, the routes audited, and whether
     you audited local production or the public URL

   After that section, include:
   - the fixes, each with the audit ID that motivated it
   - the findings you skipped, with reasons
   - which checks you ran, with results

   If T3 PR tools are available, link the PR. If nothing worth changing was
   found, open no PR, report the scores and why, and go to step 11.
10. **Approve, wait for CI, and merge.** Harry authorizes this merge for
   Lighthouse audit PRs. It doesn't extend to any other PR or action.
   - **Approve:** if the PR author is the account `gh` is signed in as
     (`gh api user --jq .login`), GitHub won't allow approving your own PR.
     Skip approval and say so in the report. Otherwise run
     `gh pr review --approve`.
   - **CI:** CI applies when `gh pr checks` lists checks or
     `.github/workflows` runs on `pull_request`. In T3, call
     `watch_pull_request` and end your turn; T3 wakes you when checks settle.
     Outside T3, run `gh pr checks --watch`. Wait for every check to finish.
   - **Failures:** if a check fails because of your change, fix it, push,
     and wait again. Stop after two fix attempts. If a check also fails on
     `<default>`, or the PR is blocked by requested changes, conflicts you
     cannot resolve cleanly, or branch protection, don't merge. Report the
     blocker.
   - **Merge:** once checks pass and `gh pr view --json mergeable,mergeStateStatus`
     shows it can merge, merge with the first method the repo allows
     (`gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed`),
     in the order squash, merge, rebase: `gh pr merge <number> --squash`
     (or `--merge` / `--rebase`). Never use `--admin`, bypass protections, or
     pass `--delete-branch`, which fails inside a worktree.
   - **Deploys:** merging may start the repo's automatic deployment. Don't
     start, retry, or change deployments yourself; report any deployment that
     started.
11. **Settle.** If you are running in T3, call `unwatch_pull_request` for a
   PR you watched. Then call `t3_thread_organize` with `action: "settle"` for
   this thread when the PR merged or no PR was needed. Leave the thread active
   when the work is blocked, so Harry sees it. Do not clean up the worktree.
12. **Report.** Summarize the scores, the changes, the skipped findings, the
   blockers, and the report folder. End with exactly one line:
   `PR <full URL>, head <SHA>, merged <yes|no: reason>, checks <state>` or
   `No PR: <reason>`.
<!-- END TEMPLATE -->
