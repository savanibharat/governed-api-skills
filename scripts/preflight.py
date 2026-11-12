#!/usr/bin/env python3
"""
preflight.py - verify the environment and inputs BEFORE a run (governed-api-skills). Step 0 of RUN.md.

Checks that the dependencies are present, the routing gate passes, every ENABLED repo path exists
(resolved relative to the project root, NOT the current directory), and that every supplied input
parses (JSON and YAML, with a light OpenAPI 'paths' sanity check). A missing enabled repo is a FIX,
not a note - matching what RUN.md promises.

Importable: check(inputs_dir=None, cfg_dir=None) -> (problems, notes).
Exit 0 = READY; exit 1 = fixes needed.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


def check(inputs_dir=None, cfg_dir=None):
    problems, notes = [], []
    for mod in ("yaml", "jsonschema"):
        try:
            __import__(mod)
        except ImportError:
            problems.append("missing python package: %s (run: bash start.sh)" % mod)
    if problems:
        return problems, notes
    import yaml

    cfg_dir = Path(cfg_dir) if cfg_dir else (PKG / "configuration")
    root = cfg_dir.parent  # repo paths are resolved relative to the project root

    try:
        topo = yaml.safe_load((cfg_dir / "repository-topology.yaml").read_text())
        for key, repo in (topo.get("repositories") or {}).items():
            if repo.get("enabled"):
                p = (root / repo.get("path", "")).resolve()
                if not p.exists():
                    problems.append("enabled repo '%s' path does not exist: %s (create it or set enabled: false)"
                                    % (key, repo.get("path")))
    except Exception as e:  # noqa
        problems.append("cannot read repository-topology.yaml: %s" % e)

    r = subprocess.run([sys.executable, str(PKG / "scripts" / "check_routing.py"), str(cfg_dir)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        problems.append("routing check failed:\n    " + r.stdout.strip().replace("\n", "\n    "))

    if inputs_dir:
        d = Path(inputs_dir)
        if not d.is_dir():
            problems.append("inputs folder not found: %s" % d)
        else:
            files = [f for f in d.rglob("*") if f.is_file()]
            for f in files:
                try:
                    if f.suffix == ".json":
                        json.loads(f.read_text(encoding="utf-8"))
                    elif f.suffix in (".yaml", ".yml"):
                        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
                        if isinstance(doc, dict) and ("openapi" in doc or "swagger" in doc) and "paths" not in doc:
                            problems.append("OpenAPI file has no 'paths': %s" % f)
                except Exception as e:  # noqa
                    problems.append("invalid %s: %s (%s)" % (f.suffix, f, e))
            if not any(f.suffix in (".yaml", ".yml", ".json", ".md", ".txt") for f in files):
                notes.append("no API docs or examples found in the inputs folder")
    else:
        notes.append("no inputs folder given - pass one to check your API docs and examples")
    return problems, notes


def main() -> int:
    problems, notes = check(sys.argv[1] if len(sys.argv) > 1 else None)
    print("PREFLIGHT:", "READY" if not problems else "NOT READY")
    for n in notes:
        print("  note:", n)
    for p in problems:
        print("  FIX :", p)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
