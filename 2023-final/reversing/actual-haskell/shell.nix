{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
  packages = [(haskellPackages.ghcWithPackages (pkgs: with pkgs; [tardis transformers cabal-install MonadRandom_0_6 extra]))];
}
