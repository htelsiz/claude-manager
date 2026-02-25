{ config, lib, pkgs, ... }:

let
  cfg = config.programs.claude-code;
  types = import ../lib/types.nix { inherit lib; };
  mkHook = import ../lib/mkHook.nix { inherit pkgs lib; };
  builtinLib = import ../hooks { inherit pkgs lib mkHook; };

  # Wrap a custom hook into a store-path command string
  wrapCustom =
    name: hook:
    let
      cmd =
        if hook.python then
          "${
            mkHook.mkPythonHook {
              inherit name;
              script = hook.script;
              pythonPackages = hook.extraPythonPackages;
            }
          }"
        else
          "${
            mkHook.mkBashHook {
              inherit name;
              script = hook.script;
              runtimeInputs = hook.extraPackages;
            }
          }";
    in
    {
      inherit (hook) event matcher timeout;
      command = cmd;
      async = hook.async;
    };

  # Collect all enabled builtin hook entries
  builtinEntries = lib.concatLists (
    lib.mapAttrsToList (
      name: bcfg: if bcfg.enable or false then builtinLib.${name} bcfg else [ ]
    ) cfg.hooks.builtins
  );

  # Collect all custom hook entries
  customEntries = lib.mapAttrsToList wrapCustom cfg.hooks.custom;

  # Group entries by event -> list of matcher groups for settings.json
  groupByEvent =
    entries:
    let
      addEntry =
        acc: e:
        let
          existing = acc.${e.event} or [ ];
        in
        acc
        // {
          ${e.event} = existing ++ [
            {
              matcher = e.matcher or "";
              hooks = [
                (
                  {
                    type = "command";
                    inherit (e) command timeout;
                  }
                  // lib.optionalAttrs (e.async or false) { async = true; }
                )
              ];
            }
          ];
        };
    in
    lib.foldl' addEntry { } entries;
in
{
  options.programs.claude-code.hooks = {
    custom = lib.mkOption {
      type = lib.types.attrsOf (
        lib.types.submodule {
          options = {
            event = lib.mkOption { type = types.hookEventType; };
            matcher = lib.mkOption {
              type = lib.types.str;
              default = "";
            };
            script = lib.mkOption { type = lib.types.path; };
            python = lib.mkOption {
              type = lib.types.bool;
              default = false;
            };
            extraPythonPackages = lib.mkOption {
              type = lib.types.functionTo (lib.types.listOf lib.types.package);
              default = _: [ ];
            };
            extraPackages = lib.mkOption {
              type = lib.types.listOf lib.types.package;
              default = [ ];
            };
            timeout = lib.mkOption {
              type = lib.types.int;
              default = 10;
            };
            async = lib.mkOption {
              type = lib.types.bool;
              default = false;
            };
          };
        }
      );
      default = { };
    };

    builtins = {
      tool-guard = {
        enable = lib.mkEnableOption "tool-guard (block dangerous Bash commands)";
        denyPatterns = lib.mkOption {
          type = lib.types.listOf lib.types.str;
          default = [ ];
        };
      };
      skill-router = {
        enable = lib.mkEnableOption "skill-router (inject skill hints on session start)";
        rules = lib.mkOption {
          type = lib.types.listOf (
            lib.types.submodule {
              options = {
                keywords = lib.mkOption { type = lib.types.listOf lib.types.str; };
                skill = lib.mkOption { type = lib.types.str; };
              };
            }
          );
          default = [ ];
        };
      };
      compact-blocker = {
        enable = lib.mkEnableOption "compact-blocker (save context before compaction)";
        message = lib.mkOption {
          type = lib.types.str;
          default = "Save important context before compaction proceeds.";
        };
      };
    };
  };

  config = lib.mkIf cfg.enable {
    programs.claude-code._hooks = groupByEvent (builtinEntries ++ customEntries);
  };
}
