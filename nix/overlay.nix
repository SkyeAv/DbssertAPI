final: prev: {
  python313Packages = prev.python313Packages.override {
    overrides = pyFinal: pyPrev: {
      dbssert-api = pyFinal.buildPythonApplication rec {
        pname = "dbssert_api";
        version = "1.0.0";
        format = "pyproject";
        src = ../.;
        build-system = (with pyFinal; [
          setuptools
          wheel
        ]);
        propagatedBuildInputs = (with pyFinal; [
          pyarrow
          fastapi
          uvicorn
          polars
          duckdb
        ]);
        doCheck = false;
      };
    };
  };
}