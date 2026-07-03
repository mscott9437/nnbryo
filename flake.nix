{
  description = "Python + PyTorch Development";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:

  let
    system = "x86_64-linux";

    pkgs = import nixpkgs {
      inherit system;
      config.allowUnfree = true;
    };

    py = pkgs.python3Packages;

  in {
    devShells.${system}.default =
      pkgs.mkShell {
        packages = with pkgs; [
          # Python
          python3
          py.pip
          py.virtualenv

          # PyTorch ecosystem
          py.torch
          py.torchvision
          py.torchaudio

          # Common ML/Data Science packages
          py.numpy
          py.pandas
          py.scipy
          py.scikit-learn
          py.matplotlib
          py.jupyterlab
          py.ipykernel

          # Development tools
          py.black
          py.ruff
          py.pytest
          py.mypy

          # Native dependencies often needed by Python packages
          gcc
          pkg-config
          openssl
          zlib

          # Utilities
          git
          curl
          jq
        ];

        shellHook = ''
          export PYTHONUNBUFFERED=1

          echo ""
          echo "Python + PyTorch Environment Ready"
          echo "Python:  $(python --version)"
          echo "PyTorch: $(python -c 'import torch; print(torch.__version__)')"
          echo ""
          echo "Create a project venv with:"
          echo "  python -m venv .venv"
          echo "  source .venv/bin/activate"
          echo ""
        '';
      };
  };
}
