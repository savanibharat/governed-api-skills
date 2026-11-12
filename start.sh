#!/usr/bin/env bash
# One-step setup for governed-api-skills. Creates an isolated .venv (does NOT touch system
# Python), installs the only dependencies, and verifies the package. This is the whole install.
set -e
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
echo "==> Creating virtual environment (.venv)"
"$PY" -m venv .venv
VENV_PY=".venv/bin/python"
[ -x "$VENV_PY" ] || VENV_PY=".venv/Scripts/python.exe"   # Windows fallback

echo "==> Installing dependencies into .venv (pyyaml, jsonschema, pytest)"
"$VENV_PY" -m pip install --quiet --upgrade pip
"$VENV_PY" -m pip install --quiet pyyaml jsonschema pytest

echo "==> Verifying the package"
"$VENV_PY" scripts/validate_skill.py .
"$VENV_PY" scripts/check_routing.py configuration

echo ""
echo "Ready. Activate the environment with:"
echo "    source .venv/bin/activate"
echo "Then run the pipeline by telling Claude, or check your inputs with:"
echo "    python scripts/preflight.py <inputs-folder>"
echo "Run the self-tests any time with:  python -m pytest -q"
