# turtle use nixos so need this file
let
  pkgs = import <nixpkgs> { };
in pkgs.mkShell {
  packages = [
    (pkgs.python313.withPackages (python-pkgs: with python-pkgs; [
      pip
      django 
      python-dotenv
    ]))
  ];
}
# Run nix-shell, NOT nix shell
