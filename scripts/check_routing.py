#!/usr/bin/env python3
"""
check_routing.py - ironclad routing completeness & consistency gate (governed-api-skills).

Verifies the derived repository topology routes EVERY artifact type to an ENABLED repo and a
DEFINED destination. No artifact type may be unrouted (no guessed defaults). Run before any
routing write. Exit 0 = ok; exit 1 = problems (listed).

Importable: check(configuration_dir) -> list[str] of problems (empty == ok).

Usage:
    python check_routing.py [configuration_dir]   # defaults to ./configuration
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml


def _load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def check(cfg_dir) -> list:
    cfg = Path(cfg_dir)
    topo = _load(cfg / "repository-topology.yaml")
    routing_cfg = _load(cfg / "artifact-routing.yaml")
    types = routing_cfg.get("artifact_types", [])
    repos = topo.get("repositories", {})
    routing = topo.get("routing", {})
    problems = []
    if not types:
        problems.append("artifact-routing.yaml defines no artifact_types list")
    for t in types:
        target = routing.get(t)
        if not target:
            problems.append("UNROUTED artifact type: %s (no default allowed - route it or ask)" % t)
            continue
        if "." not in target:
            problems.append("%s: target '%s' must be 'repo.destination'" % (t, target))
            continue
        repo_key, dest_key = target.split(".", 1)
        repo = repos.get(repo_key)
        if repo is None:
            problems.append("%s: routes to unknown repo '%s'" % (t, repo_key))
            continue
        if not repo.get("enabled", False):
            problems.append("%s: routes to DISABLED repo '%s'" % (t, repo_key))
        if dest_key not in (repo.get("destinations") or {}):
            problems.append("%s: destination '%s' not defined in repo '%s'" % (t, dest_key, repo_key))
    return problems


def _gated(cfg_dir):
    cfg = Path(cfg_dir)
    topo = _load(cfg / "repository-topology.yaml")
    types = _load(cfg / "artifact-routing.yaml").get("artifact_types", [])
    routing = topo.get("routing", {})
    repos = topo.get("repositories", {})
    return [t for t in types
            if "." in (routing.get(t) or "")
            and repos.get(routing[t].split(".", 1)[0], {}).get("approval_required")]


def main() -> int:
    cfg = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "configuration")
    problems = check(cfg)
    n = len(_load(Path(cfg) / "artifact-routing.yaml").get("artifact_types", []))
    if problems:
        print("ROUTING CHECK: FAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("ROUTING CHECK: OK - %d artifact types all routed to enabled repos." % n)
    gated = _gated(cfg)
    if gated:
        print("  approval-gated (propose, do not write silently): " + ", ".join(gated))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
