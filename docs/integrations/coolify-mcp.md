# Coolify MCP connection

Recorded: 2026-11-07. Scope: Harry's Coolify endpoint and credential guidance.
Status: authenticated read-only MCP audit completed 2026-11-07; no persistent MCP client configuration installed.

## Confirmed and observed

Harry supplied `https://coolify.harryt.dev/mcp` and said he has an API token
in the Jarvis conversation on 2026-11-07. A token was later supplied through private secret entry for the read-only audit; its value is not recorded here.

Unauthenticated HTTPS probes on that date found:

- GET returned HTTP 405 with `Allow: POST`.
- A JSON-RPC `initialize` POST returned HTTP 401, `Unauthenticated.`, and
  `WWW-Authenticate: Bearer realm="mcp", error="invalid_token"`.

Use this URL as the remote MCP endpoint. The authentication challenge indicates
Bearer authentication (`Authorization: Bearer <token>`). Successful initialization,
protocol negotiation, tool inventory, token permissions, and client compatibility
remain unverified. Do not infer tools or deployment authority from this record.

## Recommended token storage on macOS

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
