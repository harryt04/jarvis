---
name: skill-copy
description: Copy (upsert) Jarvis skills from jarvis/skills into sibling Git repositories next to the Jarvis checkout, installing each for both Claude Code (.claude/skills) and Codex (.agents/skills). Use for /skill-copy, $skill-copy, or whenever Harry asks to copy, install, sync, push, or share a Jarvis skill into another local repo, even if he doesn't name this skill.
---

# Skill copy

Copy skills from this Jarvis checkout into repositories that sit beside it on the current machine. The user chooses which skills go into which repos. A request to create or edit this skill is not a request to run it.

## 1. Discover

Run `scripts/discover.sh` from this skill folder. It prints two numbered catalogs:

- **Skills** (`S1`, `S2`, …): every `skills/<name>/SKILL.md` in this Jarvis checkout except `skill-copy`, with a short description.
- **Repos** (`R1`, `R2`, …): every Git repo in the folder that holds the primary Jarvis checkout. The script resolves the primary checkout through Git, so `../` still means the real sibling folder (`~/Documents/git` here) when you run it from a Treehouse or other linked worktree. Set `SKILL_COPY_PARENT=/path` to scan a different folder. Existing `claude`/`codex` skill folders are noted.

The numbers come from this run's alphabetical order only, so don't reuse numbers from an earlier run.

## 2. Ask

Show both catalogs exactly as printed, then give this copy-pasteable template in a fenced `markdown` block and stop to wait for the answer:

```markdown
## skill-copy plan
<!-- One line per repo: R<id>: S<id>, S<id>   ("all" works on either side) -->
- R1: S1, S3
- R4: all
```

Accept loose variants such as `3: 1,2`, ranges (`S1-S3`), skill or repo names, and `all: S2`. If any line is ambiguous or names an ID that doesn't exist, ask about that line instead of guessing.

## 3. Confirm with a dry run

Expand the answer into (skill, repo) pairs. For each pair, run:

```bash
scripts/copy.sh <jarvis_root> <skill_name> <repo_path> --dry-run
```

Combine the output into one per-repo preview. It lists files to `add` or `update`, plus target files that will be `kept` because the source doesn't have them. Flag a repo that has uncommitted changes in its skill folders (`git -C <repo> status --short -- .claude/skills .agents/skills`), because overwriting them would lose work. Ask for confirmation once for the whole plan. Skip pairs with no changes.

## 4. Copy and report

Run the same commands without `--dry-run`. Each copy upserts the skill into both `<repo>/.claude/skills/<name>/` and `<repo>/.agents/skills/<name>/`, so Claude Code and Codex both discover it. It adds and overwrites files and never deletes anything. If one path is a symlink to the other, the copy lands in a single place, which is fine.

Report a per-repo summary: skills written, files added/updated/kept, and `git -C <repo> status --short`. Don't commit, push, or open PRs in target repos unless Harry asks. Copies are snapshots: re-run this skill to refresh them. Jarvis's `skills/` stays the source of truth, so make edits there and not in the copies.
