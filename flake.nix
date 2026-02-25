{
  description = "Declarative Claude Code configuration via Home Manager";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    {
      overlays.default = final: _prev: {
        cchooks = final.callPackage ./pkgs/cchooks { };
      };

      # Library functions for building hooks
      lib =
        let
          # These need pkgs, so consumers call: claude-manager.lib.mkHookLib pkgs
          mkHookLib =
            pkgs:
            let
              lib = pkgs.lib;
              mkHook = import ./lib/mkHook.nix { inherit pkgs lib; };
              builtinHooks = import ./hooks { inherit pkgs lib mkHook; };
            in
            {
              inherit mkHook builtinHooks;
              types = import ./lib/types.nix { inherit lib; };
            };
        in
        { inherit mkHookLib; };

      homeModules = {
        claude-manager = import ./modules;
        default = import ./modules;
      };
    };
}
