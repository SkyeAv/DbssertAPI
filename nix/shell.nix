{pkgs, lib, config, ...}: 
let 
  py = pkgs.python313Packages;
in {
  packages.default = py.dbssert-api;
  devShells.default = pkgs.mkShell {
    packages = (with py; [
      dbssert-api
      python
      flake8
      pip
    ]) ++ (with pkgs; [
      duckdb
    ]);
  };
}