#!/usr/bin/env python3
"""
preflight.py - verify the environment and inputs BEFORE a run (governed-api-skills).

Step 0 of RUN.md. Checks that the only two dependencies are present, the repository topology is
sound (routing gate), the configured repo paths resolve, and every supplied input parses.
Exit 0 = READY; exit 1 = something to fix (listed).

Usage:
    python preflight.py [inputs_dir]
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # package root


def main() -> int:
    problems = []
    notes = []

    # 1. dependencies
    for mod in ("yaml", "jsonschema"):
        try:
            __import__(mod)
        except ImportError:
            problems.append("missing python package: %s  (run: bash start.sh)" % mod)

    # 2. topology + configured repo paths
    if "yaml" not in sys.modules:
        try:
            import yaml  # noqa
        except ImportError:
            yaml = None
    try:
        import yaml
        topo = yaml.safe_load((HERE / "configuration" / "repository-topology.yaml").read_text())
        for key, repo in (topo.get("repositories") or {}).items():
            if repo.get("enabled") and not Path(repo.get("path", "")).exists():
                notes.append("repo '%s' path not found yet: %s" % (key, repo.get("path")))
    except Exception as e:  # noqa
        problems.append("cannot read repository-topology.yaml: %s" % e)

    # 3. routing completeness gate
    r = subprocess.run([sys.executable, str(HERE / "scripts" / "check_routing.py"), str(HERE / "configuration")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        problems.append("routing check failed:\n    " + r.stdout.strip().replace("\n", "\n    "))

    # 4. inputs
    if len(sys.argv) > 1:
        d = Path(sys.argv[1])
        if not d.is_dir():
            problems.append("inputs folder not found: %s" % d)
        else:
            files = [f for f in d.rglob("*") if f.is_file()]
            for f in files:
                if f.suffix == ".json":
                    try:
                        json.loads(f.read_text(encoding="utf-8"))
                    except Exception as e:  # noqa
                        problems.append("invalid JSON: %s (%s)" % (f, e))
            if not any(f.suffix in (".yaml", ".yml", ".json", ".md", ".txt") for f in files):
                notes.append("no API docs or examples found in the inputs folder")
    else:
        notes.append("no inputs folder given - pass one to check your API docs and examples")

    print("PREFLIGHT:", "READY" if not problems else "NOT READY")
    for n in notes:
        print("  note:", n)
    for p in problems:
        print("  FIX :", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
