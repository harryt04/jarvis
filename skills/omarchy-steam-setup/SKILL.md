---
name: omarchy-steam-setup
description: Install Steam on an Omarchy machine and get it to the sign-in window, including the muvm and FEX route that Apple Silicon needs. Use when setting up Steam or gaming on Omarchy, or when Steam on Omarchy segfaults, exits right after its update, or never shows a window.
---

# Omarchy Steam setup

Done means a Hyprland window with class `steam` and title `Sign in to Steam`, started from the app launcher entry. Signing in is Harry's step.

Run `uname -m` on the target first.

- `x86_64`: run `omarchy-install-gaming-steam` and check for the window. The rest of this skill is the `aarch64` route.
- `aarch64`: Apple Silicon under Asahi. Follow the steps below.

## Why aarch64 needs a different route

The `steam` package ships Valve's native arm64 client at `/usr/bin/steam`. On an M2 with a 16K page kernel it segfaulted at startup (`steamrtarm64/steam`, steam 1.0.0.87-1, 2026-11-27). The route that works runs Valve's x86 client inside a muvm virtual machine under the FEX emulator. `omarchy-launch-steam` takes that route only when `~/.local/share/fex-steam/steam-launcher/bin_steam.sh` exists, and falls back to the segfaulting native client otherwise.

## Steps

### 1. Install the packages

These need sudo. Get the password through the session's secret-entry tool.

```sh
sudo pacman -S --needed steam omarchy-steam-fex FEX-Emu muvm \
  fex-emu-rootfs-arch mesa-fex-emu-overlay-i386 mesa-fex-emu-overlay-x86_64
```

`fex-emu-rootfs-arch` is a 790 MiB download from GitHub releases and took 40 minutes at the observed speed. Run pacman in the foreground or as a background job with a limit above an hour. A pacman killed mid-download leaves a stale lock and a `.part` file; see [recovery](#recovery).

Done when `pacman -Q` lists all seven packages.

### 2. Run the user-level setup

```sh
scripts/setup_user.sh
```

It needs no sudo and skips work already done. It extracts Valve's x86 launcher into `~/.local/share/fex-steam/steam-launcher`, installs `scripts/steam-fex` into `~/.local/bin`, and points `~/.local/share/applications/steam.desktop` at `steam-fex`. It leaves a customized desktop entry alone and prints its `Exec` line, so repoint that one by hand.

`steam-fex` is `omarchy-launch-steam` plus `dbus-run-session` inside the VM. Steam's 64-bit client re-executes itself in the Steam Runtime container and exits when the guest has no D-Bus session bus. `omarchy-steam-fex` 1.0.0-4 does not start one. Check whether a newer `omarchy-launch-steam` does before installing the wrapper on a later version.

### 3. Smoke-test FEX

muvm does not pass the guest's output back, so write it to a file:

```sh
muvm -- FEXBash -c 'exec >"$1" 2>&1; uname -m; ls /usr/share/vulkan/icd.d' x /path/to/out.txt
```

Done when the file shows `x86_64` and both `asahi_icd.i686.json` and `asahi_icd.x86_64.json`.

### 4. First launch

```sh
setsid nohup systemd-inhibit --what=idle steam-fex >~/.local/share/fex-steam/launch.log 2>&1 </dev/null &
```

The first launch downloads and installs two client updates of about 500 MB each, and Steam restarts itself between them. Follow `~/.local/share/Steam/logs/bootstrap_log.txt`. Keep the machine awake until the window appears, because a suspend during `Installing update...` ended in `Failed to apply update, reverting...`. Launching again applied the update.

Done when `hyprctl clients` shows class `steam` with title `Sign in to Steam`. Then tell Harry it is ready for sign-in.

## Reading the logs

Steam's own logs are in `~/.local/share/Steam/logs/`. Start with `console-linux.txt` and `bootstrap_log.txt`.

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Segmentation fault ... steamrtarm64/steam` | Native arm64 client ran | Step 2, then launch with `steam-fex` |
| `steam-runtime-launcher-service: E: Can't find session bus`, then `ReexecSteamLinux: exiting` | No D-Bus session bus in the VM | Launch with `steam-fex`, not `omarchy-launch-steam` |
| `BCommitUpdatedFiles: failed to process`, then `Failed to apply update, reverting...` | Machine suspended during the update | Launch again with idle sleep inhibited |
| `Verification skipped` followed by `Shutdown` in `bootstrap_log.txt` | Normal. The updater handed over to the client | Read `console-linux.txt` for what happened next |

These lines in the muvm output are noise: `environment variable not found`, `No IPv6 nameserver available`, `hidpipe_server ... Permission denied`, `Couldn't connect flow socket: Network is unreachable` for IPv6 addresses, and `Failed to connect to socket /run/dbus/system_bus_socket`.

## Recovery

A pacman that died mid-download leaves `/var/lib/pacman/db.lck` and `/var/cache/pacman/pkg/download-*/<package>.part`, owned by `alpm`.

1. Confirm with `pgrep -a pacman` that no pacman is running. Remove the lock only then.
2. Either rerun step 1, or resume the partial file. To resume, copy the `.part` out as the user, get the URL from `pacman -Sp fex-emu-rootfs-arch`, and run `curl -C - -o <file> <url>`. Fetch `<url>.sig` and check it with `pacman-key --verify <file>.sig <file>`. Install with `sudo pacman -U <file>` once the signature is good.

## Verification limits

Observed 2026-11-27 on one M2 MacBook running Omarchy with the `asahi-alarm` repository, kernel 7.2.11, FEX-Emu 2604-1, muvm 0.7.0-1, omarchy-steam-fex 1.0.0-4, and Steam client build 1794536281. The run reached the sign-in window. Signing in, downloading a game, and running one were not exercised. The x86_64 branch was not exercised. `setup_user.sh` pins launcher tarball 1.0.0.81, the one tested; `STEAM_LAUNCHER_URL` overrides it.
