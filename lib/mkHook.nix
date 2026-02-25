{ pkgs, lib }:
rec {
  mkPythonHook =
    {
      name,
      script,
      pythonPackages ? (_: [ ]),
    }:
    let
      python = pkgs.python3.withPackages pythonPackages;
    in
    pkgs.writeScript "claude-hook-${name}" ''
      #!${python}/bin/python3
      ${builtins.readFile script}
    '';

  mkBashHook =
    {
      name,
      script,
      runtimeInputs ? [ ],
    }:
    let
      path = lib.makeBinPath (runtimeInputs ++ [ pkgs.coreutils pkgs.jq ]);
    in
    pkgs.writeScript "claude-hook-${name}" ''
      #!${pkgs.bash}/bin/bash
      export PATH="${path}:$PATH"
      ${builtins.readFile script}
    '';
}
