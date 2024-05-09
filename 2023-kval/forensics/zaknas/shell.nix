let
  pkgs = import <nixpkgs> {};
  py-pkgs = p: with p; [
    pillow
  ];
in
pkgs.mkShell {
  packages = [
    (pkgs.python39.withPackages py-pkgs)
  ];
}
