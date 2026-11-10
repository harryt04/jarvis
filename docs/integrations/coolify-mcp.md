# Coolify MCP connection

Recorded: 2026-11-07. Updated: 2026-11-09. Scope: Harry's Coolify endpoint, credential location, and how agents use it.
Status: authenticated MCP audit and authorized deployment recovery on 2026-11-07. On 2026-11-09 the token was stored at the user level on the Linux workstation (below). No persistent harness MCP configuration is installed.

## Quick start for agents (2026-11-09)

1. **Find the token.** Look for `~/.jarvis/secrets/coolify-mcp-token`, a single-line file (directory `0700`, file `0600`). Harry chose this location on 2026-11-09 for his Linux workstation, which runs agents in the T3 Code harness. If the file is missing on a device, follow step 2. Never print, echo, copy into Git, or log its contents.
2. **If the token is missing, ask for it securely.** In T3, call `request_secret` with `delivery: "file"`, then copy the returned private file into place with `umask 077`, `mkdir -p ~/.jarvis/secrets`, `chmod 700`, and `chmod 600`. Never ask for the token in chat. If the user declines, use non-credentialed evidence such as response headers and say so.
3. **Use the token without exposing it.** Read it into a shell variable in the same command that uses it, `T="$(cat ~/.jarvis/secrets/coolify-mcp-token)"`, and send it as `Authorization: Bearer $T`. Do not enable shell tracing.
4. **Call MCP over HTTP.** POST JSON-RPC to `https://coolify.harryt.dev/mcp` with `Content-Type: application/json` and `Accept: application/json, text/event-stream`. Send `initialize`, then `tools/list` or `tools/call` (`{"name": "<tool>", "arguments": {}}`). On 2026-11-09 the server returned no `Mcp-Session-Id`, and calls worked without one. Responses may be SSE-framed, so parse from the first `{`.
5. **Or call the REST API.** `GET https://coolify.harryt.dev/api/v1/...` accepts the same Bearer token. For example, `/api/v1/applications` includes `git_branch` and `build_pack`; the MCP `list_applications` summary omits those.
6. **Start with read tools:** `coolify_help`, `get_infrastructure_overview`, `list_applications` (each entry includes `environment_name`), `list_deployments`, `get_logs`, and `list_env_keys` (names only).

### Authority boundary

The 2026-11-09 tool inventory shows this token has **full team write scope**. That covers `deploy`, `control` (start/stop/restart), `rollback_application`, create, update, and delete actions (`manage_*`, `create_*`), and `get_env_values`, which returns secret values. Having the token does not authorize using it. Without Harry's explicit request for that action in the current task, agents may use read and list tools only. Never call `get_env_values` unless Harry asked for that value. Changes to a deployed app go through its repository's normal Git/PR flow, and Coolify deploys from the configured branch.

### Production inventory snapshot, 2026-11-09

All apps are in the Coolify project `web-hosting`. In the `production` environment, apps deploy from `master`, except `hair-n-there` and `repo-staff`, which deploy from `main`. Production apps: VoiceBridge, blockparty-prod, grub-roulette, hair-n-there, harryt.dev (portfolio), kanji-forge prod, mail-flow, pantry-iq prod, platter-prod, repo-staff, riseabovedrone, route roulette, tokei, and wiki. Two use legacy repository names that GitHub redirects: `pantry-iq prod` → `harryt04/pantry-iq-landing` (now `pantry-iq`), and `wiki` → `harryt04/markdown-webserver` (now `wiki`). Beta apps deploy from branch `gnhf`. Sunshine Flower Bar is served by Vercel, not Coolify. This is a snapshot: re-list before relying on it.

## Confirmed and observed

Harry supplied `https://coolify.harryt.dev/mcp` and said he has an API token
in the Jarvis conversation on 2026-11-07. A token was later supplied through private secret entry for the read-only audit; its value is not recorded here.

Unauthenticated HTTPS probes on that date found:

- GET returned HTTP 405 with `Allow: POST`.
- A JSON-RPC `initialize` POST returned HTTP 401, `Unauthenticated.`, and
  `WWW-Authenticate: Bearer realm="mcp", error="invalid_token"`.

Use this URL as the remote MCP endpoint. The authentication challenge indicates
Bearer authentication (`Authorization: Bearer <token>`). *(Superseded 2026-11-09:
authenticated `initialize` returned HTTP 200 with Coolify MCP server 0.3.0 and
protocol `2025-06-18`. `/api/v1/version` also returned 200. See Quick start for
the tool inventory and authority boundary. Client-native MCP wiring is still unverified.)*

## Recommended token storage on macOS

*Historical recommendation from 2026-11-07. On a device where `~/.jarvis/secrets/coolify-mcp-token` exists, that file is the token location (see Quick start). Keychain remains an option on a Mac that has not been provisioned.*

Store the token in **macOS Keychain**, outside the Jarvis repository. This is a
recommendation, not a claim that a credential has already been installed.

In Keychain Access, choose the login keychain and create a new password item:

- Keychain Item Name (service): `jarvis.coolify.mcp`
- Account Name: your macOS login username (`whoami` shows it)
- Password: paste the Coolify API token

Keep the token out of chat, Git, Markdown, machine TOML, and shell history.
On another device, provision it separately through that device's credential store.
The item name above is a lookup convention, not a second copy of the secret.

## Client wiring, still to configure

Configure the chosen MCP client's remote HTTP connection with the endpoint above
and a Bearer token read from its supported credential mechanism. When the client
supports a token environment variable, use the proposed name `COOLIFY_MCP_TOKEN`.
An environment variable is only a delivery mechanism; Keychain remains the store.

For a local launcher, the Keychain value can be loaded without printing it:

```sh
export COOLIFY_MCP_TOKEN="$(security find-generic-password -s jarvis.coolify.mcp -a "$(whoami)" -w)"
# Start the MCP client from this shell, using its supported token-env setting.
unset COOLIFY_MCP_TOKEN
```

Avoid shell tracing when loading credentials. Do not paste the retrieval command
without command substitution: that would print the token. A GUI client may not
inherit this shell environment; verify its documented secret configuration before
claiming the connection is installed. No client-specific configuration is implied
by this example.

After configuring a client, verify authenticated initialization and inspect its
advertised tools before using them. Record verification date and limits here,
without capturing token values or private infrastructure responses.

Related: [storage boundaries](../setup-plan.md#storage-and-ownership) and
[provider loading](../research/provider-loading.md).

## Deployment and analytics follow-up, 2026-11-07

Harry confirms Coolify hosts his deployments. Authenticated MCP initialization and read tools worked for the audit. See the [recovery plan](../research/coolify-deployment-recovery-2026-11-07.md) for scoped live findings and analytics guidance. The earlier unauthenticated probes remain historical evidence. macOS Keychain storage above is still a recommendation, not a completed credential installation.
