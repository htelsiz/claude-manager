{
  pkgs,
  lib,
  mkHook,
}:

let
  patchScript =
    script: args:
    pkgs.writeScript "patched-${baseNameOf script}" ''
      #!${pkgs.python3}/bin/python3
      import sys
      sys.argv = [sys.argv[0]] + ${builtins.toJSON args}
      ${builtins.readFile script}
    '';
in
{
  tool-guard =
    cfg:
    [
      {
        event = "PreToolUse";
        matcher = "Bash";
        command = "${patchScript ./tool-guard.py [ (builtins.toJSON cfg.denyPatterns) ]}";
        timeout = 5;
      }
    ];

  skill-router =
    cfg:
    [
      {
        event = "SessionStart";
        matcher = "";
        command = "${patchScript ./skill-router.py [ (builtins.toJSON cfg.rules) ]}";
        timeout = 5;
      }
    ];

  compact-blocker =
    cfg:
    [
      {
        event = "PreCompact";
        matcher = "";
        command = "${
          mkHook.mkBashHook {
            name = "compact-blocker";
            script = ./compact-blocker.sh;
          }
        } ${lib.escapeShellArg cfg.message}";
        timeout = 5;
      }
    ];
}
