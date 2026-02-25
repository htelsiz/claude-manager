{ config, lib, ... }:

let
  cfg = config.programs.claude-code;

  # Assemble final JSON — only include non-empty sections
  json =
    cfg.settings
    // lib.optionalAttrs (cfg._hooks != { }) { hooks = cfg._hooks; }
    // lib.optionalAttrs (cfg._mcpServers != { }) { mcpServers = cfg._mcpServers; }
    // lib.optionalAttrs (cfg._enabledPlugins != { }) { enabledPlugins = cfg._enabledPlugins; };
in
{
  options.programs.claude-code = {
    enable = lib.mkEnableOption "Claude Code declarative configuration";

    settings = lib.mkOption {
      type = lib.types.attrsOf lib.types.anything;
      default = { };
      description = "Top-level settings merged into settings.json root.";
    };

    # Internal assembly points — populated by submodules
    _hooks = lib.mkOption {
      type = lib.types.anything;
      default = { };
      internal = true;
    };
    _mcpServers = lib.mkOption {
      type = lib.types.anything;
      default = { };
      internal = true;
    };
    _enabledPlugins = lib.mkOption {
      type = lib.types.attrsOf lib.types.bool;
      default = { };
      internal = true;
    };
  };

  config = lib.mkIf cfg.enable {
    home.file.".claude/settings.json".text = builtins.toJSON json;
  };
}
