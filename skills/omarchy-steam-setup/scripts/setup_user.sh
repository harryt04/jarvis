#!/bin/bash
# User-level half of Steam setup on an Apple Silicon Omarchy machine.
# Needs no sudo and is safe to rerun: each stage skips work already done.
#
#   1. Fetch Valve's x86 launcher into ~/.local/share/fex-steam/steam-launcher,
#      the path omarchy-launch-steam looks for before it falls back to the
#      native arm64 client.
#   2. Install the steam-fex wrapper into ~/.local/bin.
#   3. Point the user's Steam desktop entry at steam-fex.
#
# STEAM_LAUNCHER_URL overrides the pinned launcher tarball.

set -euo pipefail

url="${STEAM_LAUNCHER_URL:-https://repo.steampowered.com/steam/archive/stable/steam_1.0.0.81.tar.gz}"
here="$(cd -P "$(dirname "$0")" && pwd)"
dest="$HOME/.local/share/fex-steam"
files=(steam-launcher/bin_steam.sh
  steam-launcher/bootstraplinux_ubuntu12_32.tar.xz
  steam-launcher/steam_subscriber_agreement.txt)

if [[ $(uname -m) != aarch64 ]]; then
  echo "not aarch64: use omarchy-install-gaming-steam instead" >&2
  exit 1
fi

missing=0
for f in "${files[@]}"; do [[ -s $dest/$f ]] || missing=1; done

if ((missing)); then
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  curl -fsSL -o "$tmp/steam.tar.gz" "$url"
  mkdir -p "$dest"
  tar -xzf "$tmp/steam.tar.gz" -C "$dest" "${files[@]}"
  printf '%s' "$url" >"$dest/version"
  echo "launcher: extracted from $url"
else
  echo "launcher: already present"
fi

mkdir -p "$HOME/.local/bin"
if cmp -s "$here/steam-fex" "$HOME/.local/bin/steam-fex"; then
  echo "steam-fex: already installed"
else
  install -m 755 "$here/steam-fex" "$HOME/.local/bin/steam-fex"
  echo "steam-fex: installed to ~/.local/bin"
fi

desktop="$HOME/.local/share/applications/steam.desktop"
if [[ ! -e $desktop && ! -L $desktop ]]; then
  mkdir -p "$(dirname "$desktop")"
  cat >"$desktop" <<'DESKTOP'
[Desktop Entry]
Name=Steam
Comment=Application for managing and playing games on Steam
Exec=steam-fex %U
Icon=steam
Terminal=false
Type=Application
Categories=Network;FileTransfer;Game;
MimeType=x-scheme-handler/steam;x-scheme-handler/steamlink;
DESKTOP
  echo "desktop entry: created"
elif grep -q '^Exec=steam-fex ' "$desktop"; then
  echo "desktop entry: already uses steam-fex"
elif grep -q '^Exec=omarchy-launch-steam %U$' "$desktop"; then
  sed -i 's|^Exec=omarchy-launch-steam %U$|Exec=steam-fex %U|' "$desktop"
  echo "desktop entry: repointed to steam-fex"
else
  echo "desktop entry: customized, left alone: $(grep '^Exec=' "$desktop")"
fi
