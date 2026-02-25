{ config, lib, ... }:

let
  cfg = config.programs.claude-code;
in
{
  options.programs.claude-code.instructions = lib.mkOption {
    type = lib.types.nullOr lib.types.lines;
    default = null;
    description = "Global instructions written to ~/.claude/CLAUDE.md.";
  };

  config = lib.mkIf (cfg.enable && cfg.instructions != null) {
    home.file.".claude/CLAUDE.md".text = cfg.instructions;
  };
}
