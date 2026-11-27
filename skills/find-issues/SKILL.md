---
name: find-issues
description: "Find and verify unreported, unclaimed bugs and worthwhile performance improvements in a repository. Use for issue hunting or contribution discovery. Return evidence and a proven fix without filing issues or PRs."
---

# Find issues

Find problems worth fixing, not reasons to make changes. A retained finding needs a real affected workflow, current reproduction, no public duplicate or active owner found, and a demonstrated improvement.

This is the shared discovery and verification workflow. Ordinary use returns findings and evidence without publishing or changing the user's working tree. Use an isolated checkout for experimental patches. [find-issues-make-pr](../find-issues-make-pr/SKILL.md) adds automatic publication when the user requests it. Its publication instructions override only this report-only default.

## 1. Establish the target

- Resolve the repository, canonical upstream, intended base branch, supported environment, and requested scope from the task and current project. Read repository instructions and contribution requirements. Preserve unrelated changes.
- Inspect current upstream code and recent commits, using a separate checkout when the current worktree has unrelated work. Record the baseline commit and installed versions. Do not diagnose a shipped capability from an obsolete checkout.
- Map the relevant user paths, state transitions, failure boundaries, and hot paths. Prioritize concrete correctness, usability, reliability, or resource costs over style preferences and speculative compatibility.

Finish when the target, current baseline, realistic affected workflows, and verification commands are explicit. If no repository can be inferred or access is missing, identify that specific blocker.

## 2. Check whether the work is already known or owned

For each promising candidate, use the host's live search or API, not only local history. Search the canonical repository's open and closed issues and PRs, including drafts, abandoned or rejected proposals, relevant merged fixes, and comments or linked work. Include discussions or roadmaps when that project uses them to claim work.

Search by symptom and user-facing behavior as well as affected symbols and root cause. Read plausible matches. Check assignments, claims in comments, linked branches, recent fixes, and active PRs. An unassigned issue can still have an owner. A closed report is still a report of the same problem.

Record the search time, queries, and relevant links. Reject work already reported, fixed, or actively covered unless the user specifically requests it. If duplicate or ownership checks are unavailable or inconclusive, hold the candidate rather than presenting it as unclaimed. Repeat the search before final delivery or publication.

Finish when the evidence supports "no public report or active work found in the checked sources as of this time." Private or undisclosed work cannot be ruled out; never claim otherwise.

## 3. Prove the problem matters

Trace the cause through the current code and reproduce the behavior on the recorded baseline in a supported, plausible workflow. Distinguish a project defect from local configuration, missing dependencies, unsupported use, stale tooling, and an automated warning.

Show who encounters it, under what normal conditions, and the actual consequence. A contrived input or theoretical race alone does not establish a worthwhile contribution. Existing contracts or a representative workload can establish impact without an existing reporter.

For performance, measure the actual cost before proposing an optimization. Use comparable builds, inputs, hardware, settings, and cache conditions. Repeat trials with warmup where appropriate, report the spread and sample count, and separate the effect from noise. Relate the gain to the frequency or scale of real use. A smaller line count or a single faster run is not a performance result.

Finish when a reproducible baseline and concrete user impact are documented. Drop candidates that cannot be substantiated; report useful blocked leads separately from verified findings.

## 4. Prove the smallest improvement

Read and use [code-with-restraint](../code-with-restraint/SKILL.md) before writing a candidate fix. Keep the patch focused on the demonstrated cause, existing abstractions, and required contracts.

In the isolated checkout, apply the smallest fix that can demonstrate the improvement. Run the same reproduction on baseline and patch. Protect the important behavior with a focused regression test where appropriate. Check likely adjacent failures and update affected documentation. For optimizations, preserve observable behavior and measure costs shifted to memory, startup, allocations, or other operations.

Create an easy before/after comparison appropriate to the result: matching screenshots, a short video for motion or interactions, a benchmark table, or exact input/output and error results. Compare the same scenario and settings. Inspect the final artifact, not only a successful test or render command. Mute local playback unless the user asks to hear it. Keep private data out of shareable evidence.

Finish when the baseline demonstrates the problem, the patch demonstrates a useful correction, relevant checks pass, and the comparison supports the claim. Without this proof, the candidate is not ready to recommend or publish.

## 5. Return the verified findings

For each retained finding, provide:

- The affected workflow, impact, baseline commit/environment, and source locations.
- Reproduction steps or benchmark commands and the observed baseline result.
- The focused fix and regression checks, with before/after evidence and measured limitations.
- The public duplicate/ownership search, its time, relevant links, and any residual uncertainty.
- The local patch or checkout location and the next concrete action.

Summarize covered areas and meaningful limitations. Zero verified findings is a valid result. Do not turn every suspicion into an issue, infer that the whole project is issue-free, or keep searching merely to fill a quota. Preserve useful proof in the task's working directory and identify obsolete owned scratch files for authorized cleanup.
