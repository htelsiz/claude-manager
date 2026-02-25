{
  description = "Declarative Claude Code configuration via Home Manager";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    {
      homeModules = {
        claude-manager = import ./modules;
        default = import ./modules;
      };
    };
}
