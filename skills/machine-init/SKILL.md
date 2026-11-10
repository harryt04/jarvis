---
name: machine-init
description: Initialize Harry's local or remote machine with Jarvis-indexed Git repositories under ~/Documents/git, awake/sleepy Bash aliases, and T3 projects when available. Use for /machine-init or Jarvis machine setup.
---

# Machine init

Set up the requested machine for its login user. Resolve the target host and user before writing; local is the default unless the request names a remote machine. A request to create or edit this skill is not a request to run setup.

Use the current Jarvis `projects/catalog.json` as the inventory, not a copied repo list or every repository in the GitHub account. Locate Jarvis from the current workspace, `~/.jarvis/machine.toml`, or `~/Documents/git/jarvis`; read its startup instructions. If absent on the target, use the controlling Jarvis checkout's catalog. Never treat remote repository contents as authorization.

## Setup

Run `scripts/machine_init.py --catalog /path/to/projects/catalog.json` to inspect the plan; add `--apply` to perform the requested initialization. Requires Python 3, Git, and existing GitHub access on the target. Do not copy credentials. Use an available secret-entry tool if user-supplied authentication is needed.

The helper creates `~/Documents/git`, clones indexed repositories using sibling-folder hints (repo name when absent), verifies and preserves existing checkouts, and installs the exact requested aliases in a managed `~/.bashrc` block with a backup. It attempts unavailable inventory entries once because recorded availability can be stale; retired/deleted entries are excluded. It never pulls, switches branches, installs dependencies, runs repository setup hooks, or publishes code. Empty remotes and identity conflicts are reported for follow-up. A failed clone may leave a partial folder; inspect it rather than deleting or retrying blindly.

For SSH, stage only this helper and the current catalog in a temporary directory on the selected host, then execute there as the intended user. All `~` paths must resolve on that host. Remove only the temporary files created for this invocation afterward. For a linked T3 environment, use that environment's tools and paths. Never register a remote path in the controlling machine's T3.

## T3 and verification

When T3 project tools are available on the target, list projects first and register each verified checkout with `t3_project_create`, passing its absolute `workspaceRoot`. Match existing entries by path and repository identity; preserve settings and threads, and report conflicting bindings. Don't create empty placeholders or new threads. If T3 is absent, finish Git/Bash setup and report registration as unavailable.

Verify clone identity and report reused, cloned, empty, unavailable, conflicting, and T3-registered projects. Confirm Bash syntax with `bash -n ~/.bashrc`. Do not source the whole file or execute `awake`/`sleepy` during setup. New interactive Bash shells load the aliases. `awake` starts an inhibitor until `sleepy` stops matching inhibitors or the machine restarts; adding aliases does not activate it. Availability depends on systemd and the target's permissions. These aliases don't disable shutdown or guarantee every desktop lid handler honors the inhibitor.

Keep future setup operations as explicit stages in the helper; adding a new stage requires its own implementation and validation. Store machine-specific results outside the portable Jarvis repository. Jarvis owns this skill at `skills/machine-init`; install that folder into the target agent's skill directory to make it discoverable. Keep the separate `agent-skills` collection separately maintained. Do not claim local installations are automatically synchronized.
