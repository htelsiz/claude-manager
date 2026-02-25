{ config, lib, ... }:

let
  cfg = config.programs.claude-code;
  types = import ../lib/types.nix { inherit lib; };

  # Strip empty fields for clean JSON
  cleanServer =
    _: srv:
    { inherit (srv) command; }
    // lib.optionalAttrs (srv.args != [ ]) { inherit (srv) args; }
    // lib.optionalAttrs (srv.env != { }) { inherit (srv) env; };
in
{
  options.programs.claude-code.mcpServers = lib.mkOption {
    type = lib.types.attrsOf types.mcpServerType;
    default = { };
    description = "MCP servers to register with Claude Code.";
  };

  config = lib.mkIf cfg.enable {
    programs.claude-code._mcpServers = lib.mapAttrs cleanServer cfg.mcpServers;
  };
}
