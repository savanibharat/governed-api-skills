#!/usr/bin/env bash
# One-step setup for governed-api-skills: installs the only two dependencies and verifies the
# package. This is the whole install - no other steps, no slash commands.
set -e
cd "$(dirname "$0")"

echo "==> Installing dependencies (pyyaml, jsonschema)"
python3 -m pip install --quiet --break-system-packages pyyaml jsonschema 2>/dev/null \
  || python3 -m pip install --quiet pyyaml jsonschema

echo "==> Verifying the package"
python3 scripts/validate_skill.py .
python3 scripts/check_routing.py

echo ""
echo "Ready. Next: open RUN.md, or just tell Claude:"
echo "  Run governed-api-skills. Repositories: <skills> <mcp> <governance>. Inputs in <folder>."
