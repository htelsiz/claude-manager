{ config, lib, ... }:

let
  cfg = config.programs.claude-code;
in
{
  options.programs.claude-code.plugins = {
    marketplaces = lib.mkOption {
      type = lib.types.listOf lib.types.str;
      default = [ ];
      description = "Marketplace repos to register (owner/repo).";
    };
    install = lib.mkOption {
      type = lib.types.listOf lib.types.str;
      default = [ ];
      description = "Plugins to install (name@marketplace).";
    };
  };

  config = lib.mkIf cfg.enable {
    programs.claude-code._enabledPlugins = lib.listToAttrs (
      map (p: lib.nameValuePair p true) cfg.plugins.install
    );

    home.activation.claudePlugins = lib.mkIf (cfg.plugins.install != [ ]) (
      lib.hm.dag.entryAfter [ "writeBoundary" ] ''
        if command -v claude &>/dev/null; then
          ${lib.concatMapStringsSep "\n" (
            r: "claude plugin marketplace add ${lib.escapeShellArg r} 2>/dev/null || true"
          ) cfg.plugins.marketplaces}
          ${lib.concatMapStringsSep "\n" (
            p: "claude plugin install ${lib.escapeShellArg p} 2>/dev/null || true"
          ) cfg.plugins.install}
        fi
      ''
    );
  };
}
