---
name: security-review
description: Review Harry's Jarvis-cataloged repositories for application vulnerabilities, repair blocked or failing Dependabot upgrades, and verify production security configuration and deployed fixes. Use for a requested security review or Dependabot remediation, including reviews across active repos. Routine package vulnerability scanning remains Dependabot's job.
---

# Security review and remediation

Use agents to investigate concrete risks, prepare tested fixes, and report what
is actually deployed. Complement Dependabot rather than periodically duplicating
its package scans. This skill is an on-demand procedure, not an installed
scheduler or a claim that any repository is secure.

## Scope and authority

Honor the current request's repositories, exclusions, and review-only or fix
mode. A review-only request produces findings; a remediation request produces
PRs for verified, in-scope fixes. If the request does not distinguish these,
start with read-only investigation and clarify before making source changes.
Do not run a portfolio review merely because normal development touches auth.

Invoking this skill for multiple repositories authorizes bounded subagent
investigation within that scope. It does not authorize merges, deployments,
credential rotation, infrastructure writes, paid services, or worktree cleanup.
Use existing task authorization when it explicitly covers an action. Otherwise
prepare a concrete fix and validation evidence before requesting the applicable
approval. Do not borrow the Lighthouse skill's scoped merge authority.

Production verification is read-only by default. Do not send exploit payloads,
write test records, attempt SSRF against live internal services, or load-test
production. Reproduce vulnerabilities locally with synthetic data and isolated
services. Never print credential values or put secrets, raw logs, customer data,
or working exploit payloads in PRs, Jarvis memory, or subagent prompts. If a
credential is exposed, report a redacted location and affected scope privately;
removal alone is not rotation and cannot establish containment. Public PRs must
not disclose sensitive exploit details before coordinated remediation.

## Establish targets and delegate

1. Locate the verified Jarvis checkout, refresh its `origin/main`, and follow
   its `AGENTS.md`. Read `projects/catalog.json` and the applicable briefs.
   Jarvis paths in this skill refer to that checkout, even when the skill is
   installed elsewhere; do not infer Jarvis's location from the installed skill.
2. For "all active repos", reconcile catalog identities and aliases with the
   live owner's repository inventory and default branches. Exclude confirmed
   retired identities and archived repositories. Report inaccessible, unmapped,
   or ambiguous entries as coverage gaps; do not resurrect deleted repos or
   silently treat registry availability snapshots as current. Include applicable
   non-JavaScript repos; evaluate documentation-only repos for their actual risks.
3. Inspect existing Dependabot alerts, update-job failures, open PRs, and CI.
   Coordinate with existing owners before taking over a branch. Avoid competing
   fixes for the same issue. An existing passing security PR usually needs no
   new implementation. Missing alert access is unknown coverage, not zero risks.
4. Assign one repository per worker, in bounded batches using available slots.
   Use the user's requested provider/model, otherwise Jarvis's current confirmed
   preference. Follow the host's current delegation tools and restrictions;
   do not create new top-level threads as a substitute for subagents. Report
   unavailable settings rather than substituting a different provider/model.
   If delegation itself is unavailable and host rules permit, state the limit
   and work sequentially. An unavailable requested provider/model is not that
   fallback: report it and obtain a new choice before provider-dependent work.
5. Give each worker the [worker brief](references/worker-brief.md), verified
   repository identity, requested modes, exclusions, existing PR/alert URLs, and
   current authority. Supply metadata and credential locations, never secrets.
   Workers do not delegate again unless explicitly assigned to do so.

Each modifying worker must acquire or reuse its own Treehouse-managed task
worktree under `docs/treehouse-workflow.md` and any applicable machine workflow.
Verify the live remote and fresh base before editing; preserve unrelated work.
Read the target's current instructions and relevant source. Repository fixes,
tests, and detailed findings belong in the target repository, not Jarvis.

## Investigation modes

Run only the modes relevant to the request. A broad code-security review may
use all three, but missing production access must not block local review.

### Repair Dependabot upgrades

Start from the actual alert or failed PR, lockfile resolution, advisory, update
logs, and failing CI. Distinguish dependency-resolution errors, API changes,
required migrations, missing CI secrets, infrastructure failures, and pre-existing
test failures. Establish the relevant baseline before attributing a failure.

Check affected and patched ranges in current maintainer advisories. Upgrade to
a compatible supported version addressing the relevant advisories, with the
repository's package manager, pinning conventions, and committed lockfiles.
Update parent dependencies where needed for transitive fixes. Do not blindly
force upgrades, delete lockfiles, suppress alerts, relax security checks, or
weaken tests just to make CI green. Limit new package audits to verifying the
fix or investigating a demonstrated dependency-graph coverage gap; use the
lockfile and include indirect dependencies rather than inspecting declarations
alone. Keep dependency maintenance unrelated to the vulnerability out of scope.

Reproduce the failure and run the relevant checks after the fix, including
meaningful compatibility and authentication tests. Report residual advisories
and whether they are runtime, development-only, or not yet classified; a version
match alone does not prove an exploitable application path.

### Review application code

Trace untrusted input through actual trust boundaries to sensitive operations.
Prioritize routes handling accounts, tenant data, privileged actions, external
URLs, uploads, and credentials. Examine:

- Authentication and server-side authorization, including object ownership,
  tenant isolation, role checks, session handling, and alternate entry points.
- Secret exposure in tracked files/history where relevant, client bundles,
  build output, errors, and logs, with redacted evidence only.
- Upload validation, storage paths, serving/execution behavior, and size limits.
- SSRF through URL fetching, redirects, DNS resolution and private-address
  handling; injection, traversal, unsafe deserialization, and command execution.
- Webhook authenticity, CSRF where applicable, and abuse controls on expensive
  or privileged operations.

For each finding, identify the source revision and code location, attacker
capabilities, reachable path, impact, preconditions, and confidence. Separate
confirmed defects from hypotheses and hardening suggestions. Prefer a minimal
local reproduction and a regression test demonstrating denial of the malicious
case while preserving the legitimate case. Do not invent a CVE for a code bug.
A pattern match without a reachable path is a lead, not a confirmed finding.

### Verify production configuration and deployed fixes

Resolve the actual hosting target, application, environment, deployment branch,
and domain from live evidence. For Coolify, first read Jarvis's
`docs/integrations/coolify-mcp.md` and use only permitted read/list operations.
For other hosts, inspect their current instructions and supported read tools.

Review relevant exposure: public administrative interfaces and service ports,
TLS and trusted-proxy behavior, auth/cookie configuration, webhook protections,
and debug or secret leakage. Separate repository configuration intent from
observed live configuration; do not retrieve secret values to assess their
presence. Do not broadly scan unrelated hosts or third-party services.

Verify the expected fixed commit or artifact against the successful deployment's
revision/digest and target environment. Account for a production branch that
lags the default branch, monorepo build inputs, and upstream caches. A merged PR,
a green build, an HTTP 200, or a version header alone does not prove the fixed
artifact is serving. Use permitted non-destructive smoke checks and report the
limits of revision and application-behavior evidence separately.

An open PR alone does not establish deployment status: it may have a preview
release or a separately applied fix. If no deployment evidence exists, report
"awaiting review; deployment unverified". Otherwise name the observed artifact
and environment. If revision evidence or host access is unavailable, report
"deployment unverified".
Do not trigger or wait indefinitely for a deployment without applicable scope.
An authorized deployment follow-up follows the host's current monitoring
workflow; lack of deployment authority does not block delivery of the fix PR.

## Deliver and consolidate

Review worker findings for reachability, duplicate work, regressions, and
unnecessary scope. Each fix PR must explain the trigger and resulting behavior,
link the alert/advisory where applicable, record checks and baseline failures,
and distinguish implemented, tested, merged, and deployed states. Keep coherent
fixes together and unrelated fixes separate. Use a searchable `fix(security):`
title; apply existing repository labels only when appropriate.

Workers commit, push normally, and open or update PRs after required checks;
follow host rules for immediately linking PRs to the coordinating thread. Leave
PRs for Harry's review unless current authority explicitly permits more. Do not
close Dependabot PRs, dismiss alerts, or enable auto-merge as a side effect.

Return a concise coverage summary: each repository's inspected revision and
modes, confirmed findings and severity rationale, PR links, checks, unresolved
risks, and deployment evidence or blockers. Distinguish skipped, inaccessible,
not applicable, and inspected-with-no-confirmed-findings. Say what was not
verified rather than certifying the portfolio as vulnerability-free.

Keep raw audit artifacts and temporary coordination state under `~/.jarvis`,
with restricted permissions when sensitive, outside Git. Persist only requested
portable lessons in the existing owning Jarvis record through a separate task
PR. Do not start a schedule, install this skill, or modify account-wide security
settings merely because a review used it.
