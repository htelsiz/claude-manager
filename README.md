# claude-manager

Declarative Claude Code configuration via Nix. Provides hook builders and a built-in hook library that compiles to nix store executables.

## What it does

- **Hook builders** (`mkPythonHook`, `mkBashHook`) — wrap Python/Bash scripts into `/nix/store/` executables with correct interpreters and dependencies
- **Built-in hooks** — tool-guard (block dangerous commands), skill-router (inject skill hints), compact-blocker (save context before compaction)
- **cchooks SDK** — forked Python SDK for typed hook contexts (zero external deps)
- **Overlay** — `pkgs.cchooks` for including the SDK in Python hooks

## Usage

### With Home Manager's built-in `programs.claude-code`

Home Manager already provides a `programs.claude-code` module. Use claude-manager as a library for hook builders:

```nix
# flake.nix
{
  inputs.claude-manager = {
    url = "github:htelsiz/claude-manager";
    inputs.nixpkgs.follows = "nixpkgs";
  };
}
```

```nix
# home.nix
{ pkgs, inputs, ... }:

let
  cm = inputs.claude-manager.lib.mkHookLib pkgs;
  inherit (cm) mkHook builtinHooks;

  skillRouterEntries = builtinHooks.skill-router {
    enable = true;
    rules = [
      { keywords = ["debug" "bug"]; skill = "systematic-debugging"; }
      { keywords = ["test" "tdd"]; skill = "test-driven-development"; }
    ];
  };

  toolGuardEntries = builtinHooks.tool-guard {
    enable = true;
    denyPatterns = [ "rm -rf /" ];
  };

  # Convert entries to settings.json format
  toHookSettings = entries:
    builtins.foldl' (acc: e:
      acc // { ${e.event} = (acc.${e.event} or []) ++ [{
        matcher = e.matcher or "";
        hooks = [{ type = "command"; inherit (e) command timeout; }];
      }]; }
    ) {} entries;
in
{
  programs.claude-code = {
    enable = true;
    settings.hooks = toHookSettings (skillRouterEntries ++ toolGuardEntries);
    mcpServers.my-server = { command = "my-mcp"; args = [ "stdio" ]; };
  };
}
```

### Custom hooks

```nix
let
  myHook = mkHook.mkPythonHook {
    name = "my-hook";
    script = ./hooks/my-hook.py;       # cchooks SDK auto-included
    pythonPackages = ps: [ ps.requests ]; # extra deps
  };

  myBashHook = mkHook.mkBashHook {
    name = "my-bash-hook";
    script = ./hooks/my-hook.sh;       # jq + coreutils auto-included
    runtimeInputs = [ pkgs.curl ];      # extra deps
  };
in
{
  programs.claude-code.settings.hooks.PreToolUse = [{
    matcher = "Bash";
    hooks = [{ type = "command"; command = "${myHook}"; timeout = 5; }];
  }];
}
```

## Built-in hooks

| Hook | Event | Description |
|------|-------|-------------|
| `tool-guard` | PreToolUse | Blocks Bash commands matching deny patterns |
| `skill-router` | SessionStart | Injects skill routing rules as context |
| `compact-blocker` | PreCompact | Blocks first compaction to save context |

## cchooks SDK

```python
from cchooks import create_context

ctx = create_context()  # reads JSON from stdin, returns typed context

if ctx.hook_event_name == "PreToolUse":
    if ctx.tool_name == "Bash" and "dangerous" in ctx.tool_input.get("command", ""):
        ctx.output.deny("Blocked dangerous command")
    else:
        ctx.output.allow()
```

## License

MIT
