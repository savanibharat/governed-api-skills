#!/usr/bin/env python3
"""
check_profile.py - enforce the active workspace profile against the routing config
(governed-api-skills).

Policy: allow-but-hold. When the profile sets allow_federation_writes: false, shared / federated
artifacts must route to an APPROVAL-GATED repo (held as proposals, never silently written). This
makes workspace-profile.yaml authoritative instead of decorative, and FAILS on a silent-write
contradiction.

Importable: check(cfg_dir) -> list[str] of problems (empty == ok).
Exit 0 = ok; exit 1 = problems.
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parent.parent
SHARED_TYPES = {"proposed_shared_standard", "federated_eval"}


def _load(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def check(cfg_dir) -> list:
    cfg = Path(cfg_dir)
    prof = _load(cfg / "workspace-profile.yaml") or {}
    topo = _load(cfg / "repository-topology.yaml")
    types = _load(cfg / "artifact-routing.yaml").get("artifact_types", [])
    policies = prof.get("policies", {})
    allow_fed = policies.get("allow_federation_writes", False)
    require_approval_shared = policies.get("require_approval_for_shared_artifacts", True)
    repos = topo.get("repositories", {})
    routing = topo.get("routing", {})
    problems = []
    for t in types:
        target = routing.get(t)
        if not target or "." not in target:
            continue
        repo_key = target.split(".", 1)[0]
        repo = repos.get(repo_key, {})
        gated = repo.get("approval_required", False)
        enabled = repo.get("enabled", False)
        if t in SHARED_TYPES:
            if require_approval_shared and not gated:
                problems.append("%s routes to '%s' which is not approval_required, but the profile requires approval for shared artifacts" % (t, repo_key))
            if not allow_fed and enabled and not gated:
                problems.append("profile forbids federation writes but %s would be written (not held) to enabled, ungated repo '%s'" % (t, repo_key))
    return problems


def _holds(cfg_dir):
    cfg = Path(cfg_dir)
    topo = _load(cfg / "repository-topology.yaml")
    types = _load(cfg / "artifact-routing.yaml").get("artifact_types", [])
    repos = topo.get("repositories", {})
    routing = topo.get("routing", {})
    return [t for t in types if "." in (routing.get(t) or "")
            and repos.get(routing[t].split(".", 1)[0], {}).get("approval_required")]


def main() -> int:
    cfg = sys.argv[1] if len(sys.argv) > 1 else str(PKG / "configuration")
    problems = check(cfg)
    if problems:
        print("PROFILE: FAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("PROFILE: OK - shared artifacts are approval-gated under the active profile.")
    holds = _holds(cfg)
    if holds:
        print("  hold-only (proposal + approval, never auto-written): " + ", ".join(holds))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
