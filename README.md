<div align="center">

# claude-manager

**Declarative Claude Code hooks compiled to the Nix store.**

[![FlakeHub](https://img.shields.io/endpoint?url=https://flakehub.com/f/htelsiz/claude-manager/badge)](https://flakehub.com/flake/htelsiz/claude-manager)
[![Nix Flake](https://img.shields.io/badge/nix-flake-blue?logo=nixos&logoColor=white)](https://nixos.wiki/wiki/Flakes)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Overview](#overview) · [Quick Start](#quick-start) · [Built-in Hooks](#built-in-hooks) · [Custom Hooks](#custom-hooks) · [cchooks SDK](#cchooks-sdk) · [Architecture](#architecture)

</div>

---

## Overview

claude-manager provides **Nix-native hook builders** for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Instead of managing hook scripts manually in `~/.claude/hooks/`, you declare them in Nix — and they compile to immutable `/nix/store/` executables with pinned interpreters and dependencies.

### Why?

| Without claude-manager | With claude-manager |
|---|---|
| Hook scripts scattered in `~/.claude/hooks/` | Hooks declared in Nix, compiled to store paths |
| Python hooks need manual venv management | Python interpreter + deps pinned in derivation |
| Hooks break when system Python updates | Hooks are immutable — same Python forever |
| No way to share hooks across machines | Hooks travel with your flake config |
| Manual `settings.json` editing | `settings.json` generated declaratively |

### What's included

- **`mkPythonHook`** / **`mkBashHook`** — wrap scripts into `/nix/store/` executables with correct interpreters
- **Built-in hook library** — tool-guard, skill-router, compact-blocker (ready to enable)
- **cchooks SDK** — forked Python SDK for typed hook contexts (zero external deps, nix-packaged)
- **Overlay** — `pkgs.cchooks` for including the SDK in any Python environment

## Quick Start

### 1. Add the flake input

```nix
# flake.nix
{
  inputs.claude-manager = {
    url = "github:htelsiz/claude-manager";
    inputs.nixpkgs.follows = "nixpkgs";
  };
}
```

### 2. Pass `inputs` to Home Manager

```nix
# In your system config (NixOS or nix-darwin)
home-manager = {
  extraSpecialArgs = { inherit inputs; };
  users.youruser = import ./home.nix;
};
```

### 3. Use the hook builders in your home config

```nix
# home.nix
{ pkgs, inputs, lib, ... }:

let
  cm = inputs.claude-manager.lib.mkHookLib pkgs;
  inherit (cm) mkHook builtinHooks;

  # Enable the built-in skill router
  routerEntries = builtinHooks.skill-router {
    enable = true;
    rules = [
      { keywords = ["debug" "bug" "error"]; skill = "systematic-debugging"; }
      { keywords = ["test" "tdd"];          skill = "test-driven-development"; }
    ];
  };

  # Enable the tool guard
  guardEntries = builtinHooks.tool-guard {
    enable = true;
    denyPatterns = [ "rm -rf /" ":(){ :|:& };:" ];
  };

  # Helper: convert builtin entries to settings.json format
  toHookSettings = entries:
    lib.foldl' (acc: e: acc // {
      ${e.event} = (acc.${e.event} or []) ++ [{
        matcher = e.matcher or "";
        hooks = [{ type = "command"; inherit (e) command timeout; }];
      }];
    }) {} entries;
in
{
  programs.claude-code = {
    enable = true;
    settings.hooks = toHookSettings (routerEntries ++ guardEntries);
  };
}
```

### 4. Rebuild

```bash
# macOS
darwin-rebuild switch --flake .#myhost

# NixOS
sudo nixos-rebuild switch --flake .#myhost
```

Your `~/.claude/settings.json` now contains hooks pointing to `/nix/store/...` paths.

## Built-in Hooks

Ready-to-use hooks you can enable with a single attrset:

| Hook | Event | What it does |
|------|-------|-------------|
| **tool-guard** | `PreToolUse` | Blocks Bash commands matching regex deny patterns |
| **skill-router** | `SessionStart` | Injects keyword → skill routing rules as context |
| **compact-blocker** | `PreCompact` | Blocks first compaction so Claude saves context |

<details>
<summary><b>tool-guard</b> — block dangerous commands</summary>

```nix
builtinHooks.tool-guard {
  enable = true;
  denyPatterns = [
    "rm -rf /"                # obvious
    ":(){ :|:& };:"           # fork bomb
    "DROP TABLE"              # SQL injection
    "curl.*\\| ?sh"           # pipe to shell
  ];
}
```

When a Bash tool call matches any pattern, Claude receives:
```json
{"permissionDecision": "deny", "permissionDecisionReason": "Blocked: matches pattern 'rm -rf /'"}
```

</details>

<details>
<summary><b>skill-router</b> — auto-invoke skills by keyword</summary>

```nix
builtinHooks.skill-router {
  enable = true;
  rules = [
    { keywords = ["debug" "bug" "error" "failing"]; skill = "systematic-debugging"; }
    { keywords = ["test" "tdd" "spec"];             skill = "test-driven-development"; }
    { keywords = ["plan" "design" "architect"];      skill = "writing-plans"; }
  ];
}
```

On `SessionStart`, Claude receives additional context with the routing rules.

</details>

<details>
<summary><b>compact-blocker</b> — protect context window</summary>

```nix
builtinHooks.compact-blocker {
  enable = true;
  message = "Save important context to memory files before compaction proceeds.";
}
```

Blocks the first `PreCompact` event per session, giving Claude a chance to persist important context.

</details>

## Custom Hooks

### Python hooks

Python hooks automatically include the **cchooks SDK** — no manual dependency management:

```nix
let
  myHook = mkHook.mkPythonHook {
    name = "my-hook";
    script = ./hooks/my-hook.py;         # cchooks auto-included
    pythonPackages = ps: [ ps.requests ]; # add extra deps
  };
in
{
  programs.claude-code.settings.hooks.PreToolUse = [{
    matcher = "Bash";
    hooks = [{ type = "command"; command = "${myHook}"; timeout = 5; }];
  }];
}
```

### Bash hooks

Bash hooks automatically include `jq` and `coreutils` in `$PATH`:

```nix
let
  myHook = mkHook.mkBashHook {
    name = "my-hook";
    script = ./hooks/my-hook.sh;
    runtimeInputs = [ pkgs.curl pkgs.gh ]; # add extra tools
  };
in
{
  programs.claude-code.settings.hooks.PostToolUse = [{
    matcher = "Edit|Write";
    hooks = [{ type = "command"; command = "${myHook}"; timeout = 10; }];
  }];
}
```

## cchooks SDK

A zero-dependency Python SDK for writing typed Claude Code hooks. Forked from [GowayLee/cchooks](https://github.com/GowayLee/cchooks) and packaged as a Nix derivation.

### Usage

```python
from cchooks import create_context

ctx = create_context()  # reads JSON from stdin, returns typed context

match ctx.hook_event_name:
    case "PreToolUse":
        if "dangerous" in ctx.tool_input.get("command", ""):
            ctx.output.deny("Blocked dangerous command")
        else:
            ctx.output.allow()
    case "SessionStart":
        ctx.output.add_context("Remember to check for applicable skills.")
    case "UserPromptSubmit":
        ctx.output.add_context(f"User asked: {ctx.prompt[:100]}")
```

### Supported contexts

| Event | Context class | Key properties |
|-------|--------------|----------------|
| `PreToolUse` | `PreToolUseContext` | `tool_name`, `tool_input`, `cwd` |
| `PostToolUse` | `PostToolUseContext` | `tool_name`, `tool_input`, `tool_response` |
| `UserPromptSubmit` | `UserPromptSubmitContext` | `prompt`, `cwd` |
| `SessionStart` | `SessionStartContext` | `source` |
| `SessionEnd` | `SessionEndContext` | `reason`, `cwd` |
| `PreCompact` | `PreCompactContext` | `trigger`, `custom_instructions` |
| `Stop` | `StopContext` | `stop_hook_active` |
| `SubagentStop` | `SubagentStopContext` | `stop_hook_active` |
| `Notification` | `NotificationContext` | `message`, `cwd` |

## Architecture

```
claude-manager/
├── flake.nix              # Overlay (pkgs.cchooks) + lib exports
├── lib/
│   ├── mkHook.nix         # mkPythonHook, mkBashHook builders
│   └── types.nix          # Shared types (17 hook events, MCP server submodule)
├── hooks/
│   ├── default.nix        # Built-in hook library
│   ├── tool-guard.py      # PreToolUse: regex-based command blocking
│   ├── skill-router.py    # SessionStart: keyword → skill injection
│   └── compact-blocker.sh # PreCompact: first-compaction gate
├── pkgs/cchooks/          # Python SDK (zero deps, nix-packaged)
│   ├── default.nix        # buildPythonPackage derivation
│   ├── pyproject.toml
│   └── src/cchooks/       # 9 context types + output helpers
└── modules/               # Standalone HM module (if no upstream collision)
```

### How hooks compile

```
Nix expression                    /nix/store/ executable
─────────────                     ───────────────────────
mkPythonHook {                    /nix/store/abc...-claude-hook-my-hook
  name = "my-hook";          →    #!/nix/store/xyz...-python3/bin/python3
  script = ./my-hook.py;          <contents of my-hook.py>
}
```

The shebang points to a pinned Python with all dependencies baked in. No virtualenv, no `pip install`, no PATH manipulation.

## Real-world example

See [htelsiz/nixos-config](https://github.com/htelsiz/nixos-config/blob/main/home/claude-code.nix) for a production config with:
- 3 built-in hooks (skill-router, tool-guard, compact-blocker)
- 4 custom hooks (memory-recall, memory-store, failure-store, compact-save)
- 3 MCP servers (container-use, taskmaster-ai, appstoreconnect)
- 5 plugin marketplace installs

## License

MIT — see [LICENSE](LICENSE).

## Credits

- Hook SDK forked from [GowayLee/cchooks](https://github.com/GowayLee/cchooks) (MIT)
- Inspired by [plasma-manager](https://github.com/nix-community/plasma-manager)'s Home Manager module pattern
