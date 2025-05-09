let
  pkgs = import <nixpkgs> {};
  py-pkgs = p: with p; [
    ipython
    pycryptodome
  ];
in
pkgs.mkShell {
  packages = [
    (pkgs.python310.withPackages py-pkgs)
  ];
}

