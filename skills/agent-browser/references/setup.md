# agent-browser setup and recovery

Source: <https://agent-browser.dev/installation> and the CLI's own `--help` and
`doctor`, read 2026-11-15 with agent-browser 0.43.0. Recheck both after an
upgrade. CLI output overrides this note when they disagree.

## Install

```bash
npm install -g agent-browser   # native Rust binary via npm (pnpm/yarn/bun also work)
agent-browser install          # downloads Chrome for Testing
agent-browser doctor           # should end with "0 fail" and a passing launch test
```

On Linux x64, `agent-browser install --with-deps` also installs browser
libraries through the system package manager. It uses `sudo`, so ask before
running it. Other methods are `brew install agent-browser` (macOS),
`cargo install agent-browser`, and `npx agent-browser ...` with no install.
With mise-managed Node, the global binary lands in the active Node install.
mise reshims automatically, so `command -v agent-browser` finds it.

## Linux ARM64 (for example, Omarchy/Arch on aarch64)

Chrome for Testing has no Linux ARM64 build, so `agent-browser install` exits
with an error. Use the distribution's Chromium instead:

```bash
command -v chromium || sudo pacman -S chromium     # ask before installing
mkdir -p ~/.agent-browser
printf '{\n  "executablePath": "/usr/bin/chromium"\n}\n' > ~/.agent-browser/config.json
agent-browser doctor
```

`~/.agent-browser/config.json` is the user-level config. A project-level
`./agent-browser.json` ignores path settings by design, so the executable path
has to go in the user-level file. You can also set
`AGENT_BROWSER_EXECUTABLE_PATH` or pass `--executable-path`, but the config
file survives new shells.

Doctor may warn that the distribution's Chromium is behind current stable.
That is expected on ARM repositories that lag. Keep the system up to date to
pick up security fixes.

Observed 2026-11-15 on Harry's Omarchy aarch64 machine: npm install 0.43.0,
`install` refused (no ARM64 build), and `executablePath` pointed at Arch Linux
ARM Chromium 153. Doctor reported 11 pass, 0 fail. `open` +
`snapshot -i` on example.com and `read --outline` both worked.

## Maintenance

- `agent-browser upgrade` updates the CLI using the method it was installed
  with. Run `doctor` afterwards.
- Use `agent-browser doctor` first for `Unknown command`, `Failed to connect`,
  a stale daemon, or a missing browser. `doctor --fix` performs destructive
  repairs, so say so before running it.
- Optional: run `npx skills add vercel-labs/agent-browser` to install
  upstream's own skill. Jarvis does not depend on it, because
  `agent-browser skills get core` already serves the same guide matched to the
  installed version.
