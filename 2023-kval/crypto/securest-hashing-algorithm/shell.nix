let
  pkgs = import <nixpkgs> {};
  py-pkgs = p: with p; [
    challtools
  ];
in
pkgs.mkShell {
  packages = [
    (pkgs.python39.withPackages py-pkgs)
  ];
}
