#!/usr/bin/env bash
# Local verification - mirrors CI (.github/workflows/ci.yml, a hidden folder). Run from the
# package root. This is the visible entry point: `bash verify.sh`.
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
echo "== unit tests ==";   "$PY" -m pytest -q
echo "== conformance =="; "$PY" scripts/validate_skill.py .
echo "== routing ==";     "$PY" scripts/check_routing.py configuration
echo "== profile ==";     "$PY" scripts/check_profile.py configuration
echo "== drift ==";       "$PY" scripts/check_drift.py examples/expected
echo "== self-eval ==";   "$PY" scripts/run_evals.py
echo ""
echo "All local checks passed. (CI runs the same steps from .github/workflows/ci.yml.)"
