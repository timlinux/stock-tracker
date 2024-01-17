let
  pinnedHash = "933d7dc155096e7575d207be6fb7792bc9f34f6d"; 
  pinnedPkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/${pinnedHash}.tar.gz") { };
  pythonPackages = pinnedPkgs.python3Packages;
in pinnedPkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = [
    # A Python interpreter including the 'venv' module is required to bootstrap
    # the environment.
    pythonPackages.python
    # This executes some shell code to initialize a venv in $venvDir before
    pythonPackages.venvShellHook
    pythonPackages.pygobject3
    pythonPackages.requests
    pythonPackages.pandas
    pythonPackages.plotly
  ];
  # DIRENV_LOG_FORMAT to reduce direnv verbosity
  # See https://github.com/direnv/direnv/issues/68#issuecomment-162639262
  shellHook = ''
     export DIRENV_LOG_FORMAT=
     echo "-----------------------"
     echo "🌈 Your Python Dev Environment is ready."
     echo ""
     echo "🚀 Run:"
     echo "./stock-tracker.py"
     echo "-----------------------"
  '';
  postShellHook = ''
  '';
}
