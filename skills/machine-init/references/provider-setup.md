# Provider setup

Harry uses Codex, Claude Code, and Google Antigravity. Check the CLI and account on the target host under the target login user. If T3 uses a managed binary, a custom home, or a provider-specific environment, check the same binary and environment T3 will use. Install a missing CLI through T3's supported installer or the provider's official installation guidance for the target OS and architecture.

## Codex and Claude Code

- **Codex.** Run `codex login status`. If signed out, start `codex login` in an interactive terminal on the target. For a remote host, use `codex login --device-auth` when supported. Recheck login status after approval.
- **Claude Code.** Run `claude auth status --json` and check `loggedIn`. If signed out, start `claude auth login` in an interactive terminal on the target. Recheck status after approval.

When T3 is available, verify its built-in Codex and Claude providers are enabled and recognize those sessions. Use the provider settings to refresh status if needed.

Distinguish a missing login from a failed status check. Keep existing valid credentials and configured auth methods. Let Harry complete consent directly with the provider. If the agent has to collect a one-time code or secret, use the harness's secure secret-entry tool. Keep credential files and values on the target and out of chat, logs, settings patches, and Git.

## Google Antigravity in T3

1. Find the target's `agy` executable and confirm `agy --version` and `agy acp --help`. Upgrade from Google's official distribution if the installed version lacks ACP. T3 should launch the official Antigravity CLI over ACP.
2. Enable T3's built-in **Antigravity** provider and use the absolute path to the verified `agy` if T3 cannot resolve it. Select **Google account** for Harry's personal sign-in when setting up a new instance. If the legacy **Gemini CLI** ACP entry fails with the Gemini Code Assist for individuals migration message, disable that entry and keep its configuration and thread history.
3. Prefer T3's provider settings. For a local T3 build that uses the observed `~/.t3/userdata/settings.json` layout, back up the actual target settings file and merge the settings below into `providerInstances.antigravity`. Confirm the installed build's schema and active data directory before editing, write atomically, preserve unrelated keys and provider defaults, and verify the running T3 instance picked up the change. To disable the migrated legacy entry, use the existing registry instance key (observed as `acpRegistry_gemini_cli`). Verify the entry identifies Gemini CLI before changing it.

   ```json
   {
     "driver": "antigravity",
     "enabled": true,
     "config": {
       "enabled": true,
       "binaryPath": "/absolute/path/to/agy",
       "authMethod": "oauth-personal"
     }
   }
   ```

   The observed build reads `config.enabled` as well as the instance-level flag for Antigravity. Setting only the outer flag allowed the provider to revert to disabled. For the legacy Gemini instance, set both flags to `false` if editing that same layout.
4. Check auth by opening a fresh ACP subprocess with `agy acp`. Send `initialize` (protocol version 1), then `session/new` with an absolute target working directory and an empty MCP server list. Close the subprocess after reading the response. If it returns `Authentication required`, open an interactive `agy` terminal on the target and let Harry complete Google sign-in. For a remote terminal, use `agy acp --login` if supported. Repeat the ACP check afterward. This probe needs no model prompt or T3 thread.
5. If the ACP session returns models and T3 still shows unchecked access or an empty model list, run **Refresh provider status** in **Settings → Providers → Antigravity**. Verify the T3 provider is enabled and its picker lists the account's models. Use the discovered model list because Google plan access and model names can change.

This flow was observed on Linux ARM64 with Antigravity CLI 1.5.14. See [Google's ACP setup](https://antigravity.google/docs/cli/acp/) for current commands.

Report each provider as already signed in, newly verified, or pending with its specific blocker. Keep the machine-init thread active if sign-in or requested verification still needs Harry's input.
