{
  description = "A bare python flake";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (sys:
      let pkgs = nixpkgs.legacyPackages.${sys};
          python = pkgs.python310.withPackages (ps: with ps; [
            ipython
            pylsp-mypy
          ]);
          cfg = ./mypy-config.ini;
      in rec {
        packages.tychk-watch = pkgs.writeScriptBin "tychk" "echo 'running mypy on change...' ; ${pkgs.watchexec}/bin/watchexec -e py ${python}/bin/mypy --config ${cfg} .";
        packages.tychk = pkgs.writeScriptBin "tychk" "${python}/bin/mypy ${./.} --config ${cfg}";
        devShells.default = pkgs.mkShell {
          packages = [ python ];
        };
      }
    );
}
