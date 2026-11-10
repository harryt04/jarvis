# Security-review worker brief

Use this as the assignment template. The coordinator supplies concrete values
for the assignment fields; omit modes outside the current request.

## Assignment fields

- Verified repository identity and current default branch/base.
- Jarvis checkout location and reviewed brief pointer.
- Scope: Dependabot remediation, application-code review, production verification.
- Mode: review-only or fixes with PRs; requested exclusions and priorities.
- Existing alert, PR, CI failure, and deployment references.
- Current authority and limits, including any separately authorized live action.
- Available provider/model and applicable host delegation/PR-linking rules.

## Worker instructions

Read the security-review skill supplied by the coordinator and apply its scope,
evidence, privacy, and production boundaries. This assignment is for one repo;
do not spawn more workers unless explicitly assigned. Refresh Jarvis context as
required, then resolve the target from verified identity rather than assuming
paths from folder names or a task-worktree parent.

Inspect current target instructions, source, Git state, existing PRs, and CI.
For modifications, follow Jarvis's portable Treehouse workflow, acquiring or
resuming a durable task lease and checking its base before editing. Never reset
someone else's changes or fall back to editing the primary checkout. Use the
repository's actual package manager and checks. Coordinate before taking over
an existing PR; otherwise use an independent task branch and reference the
blocked Dependabot PR without closing or altering it.

Investigate assigned modes with local synthetic reproductions. Report only
supported findings, and do not confuse an advisory match with a reachable
production exploit. Keep sensitive evidence redacted and out of public PRs.
If a proof requires a risky live action, finish the local evidence and state
what additional authorization is required instead of executing it.

In fix mode, deliver minimal, tested patches as PRs. Record necessary checks
that fail or cannot run, with their causes. Follow current host rules for PR
linking immediately after creating, taking over, or pushing to a PR. Do not
merge, deploy, rotate credentials, dismiss alerts, close competing PRs, or clean
up worktrees without applicable current authority. Do not watch PRs from a child
agent; hand monitoring needs to the coordinator.

Return:

- Source revision, worktree/branch if modified, and exact review coverage.
- Findings with location, attacker preconditions, impact, confidence, and evidence.
- Fixes, checks, baseline failures, residual risks, and PR URLs/head SHAs.
- Production environment and observed revision/digest, safe smoke checks, and
  a separate deployed/not-deployed/unverified statement with verification time.
- Access gaps or next actions requiring Harry or the coordinator.

PR state alone does not establish deployment status; require artifact evidence.
No findings does not prove security.
After PR work, end with the host-required PR URL, head SHA, and checks/reviews
state. Keep temporary private artifacts outside the repository.
