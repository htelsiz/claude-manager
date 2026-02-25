{
  description = "Declarative Claude Code configuration via Home Manager";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    {
      overlays.default = final: _prev: {
        cchooks = final.callPackage ./pkgs/cchooks { };
      };

      homeModules = {
        claude-manager = import ./modules;
        default = import ./modules;
      };
    };
}
