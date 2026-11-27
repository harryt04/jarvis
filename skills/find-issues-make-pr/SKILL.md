---
name: find-issues-make-pr
description: "Find, verify, fix, and automatically file an issue plus PR for unreported, unclaimed repository problems. Use when explicitly invoked or when the user requests end-to-end issue discovery and publication. Uses code-with-restraint and includes before/after proof."
---

# Find issues and make PRs

Use the full [find-issues](../find-issues/SKILL.md) workflow as the single source of truth for discovery, duplicate and ownership checks, reproduction, practical impact, and verification. Read and use [code-with-restraint](../code-with-restraint/SKILL.md) for every fix. Apply the publication steps below to each finding that passes those checks.

## Authorization and scope

Invoking this skill or requesting its end-to-end workflow authorizes the verified fix, focused branch or worktree, creating or using the user's fork when needed, commit, push, issue creation, and regular PR creation against the requested repository. Finish those actions without asking the user to approve each one again.

Automatic skill selection alone is not authorization to publish. A request only to inspect, explain, suggest, or show a proposal stays read-only externally. Honor "show me first," "don't file yet," the exact repository scope, and other explicit limits. Do not merge without a separate instruction. Use the repository's private disclosure route for security findings.

## Prepare a submission that is already verified

1. Complete the shared workflow in an isolated checkout. Resolve every retained candidate to verified, rejected, or specifically blocked. Keep separate problems in separate focused changes; do not mix speculative cleanup into the fix.
2. Follow the contribution guide and inspect recent merged PRs and Git history for title and description conventions. Ensure the branch is based on the latest intended target. If the base changed, rebase or update without overwriting unrelated work, then repeat affected verification and before/after checks.
3. Build the actual issue and PR descriptions from the observed results. The issue states the affected workflow, supported environment, baseline commit, expected/actual behavior, minimal reproduction, and impact. The PR opens with that problem, explains the focused correction, and reports validation and relevant limitations. Use the repository templates.
4. Include a clear before/after comparison in the PR description whenever feasible. Match screenshots or video states for visual changes; use measured tables for performance or exact input/output for nonvisual bugs. Attach only publishable evidence. A Markdown table is a useful fallback when image/video attachments are unavailable. Local filesystem links are not usable proof for a public reviewer. If a direct comparison cannot be produced, explain the concrete limitation and provide the strongest verified evidence available.

Finish when the patch, comparison, and submission text are concrete and reviewable. Do not substitute a plan to verify later.

## File the issue and PR automatically

1. Immediately before filing, refresh the shared duplicate and ownership searches and current upstream state. Reuse a matching issue or PR already created by this run on retries. If someone else has reported or started the same work, do not create a competing submission; report the match.
2. Create the verified issue, commit and push the focused branch to the correct repository or fork, then open a regular PR against the intended base. Link the new issue with the repository's closing syntax where appropriate. File one issue/PR pair per independent verified problem. Do not publish blocked or speculative candidates to satisfy the request.
3. Immediately register each created PR with T3's `link_pull_request` when available. Before finishing, use `list_thread_pull_requests` to confirm every PR from this task is linked. Do not link unrelated background PRs.
4. Read back the issue, PR body, base/head, files, and comparison after creation. Verify attachment visibility and that the published text reflects the tested commit. Inspect available checks and fix failures caused by the change within scope. Describe pending checks as pending. If asked to monitor and T3's `watch_pull_request` is available, use it instead of polling.

If a host operation fails or its result is uncertain, inspect the remote state before retrying. Preserve returned issue/PR URLs and branch names so a retry cannot create duplicates. Continue independent local work while resolving a concrete access blocker. State any action still blocked; do not claim an issue or PR exists until the host confirms it.

Finish with the issue and PR links, the key before/after result, validation status, and any required next action. If nothing passed verification and novelty checks, report zero submissions and the checked scope. This workflow ends at a verified submission unless the user requests further work.
