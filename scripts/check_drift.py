#!/usr/bin/env python3
"""
check_drift.py - list generated skills whose baked uber_standard_version is behind the current
uber-standard/VERSION (governed-api-skills). Closes the "nobody can tell which skills are stale" gap.

Importable: check(skills_root) -> list of (name, have, want). Exit 0 = none stale; exit 1 = stale.

Usage:
    python check_drift.py [skills_root]   # defaults to the bundled examples/expected
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parent.parent


def current_version() -> str:
    return (PKG / "uber-standard" / "VERSION").read_text(encoding="utf-8").strip()


def _version_of(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    return (fm.get("metadata") or {}).get("uber_standard_version")


def check(skills_root) -> list:
    want = current_version()
    stale = []
    for md in sorted(Path(skills_root).rglob("SKILL.md")):
        have = _version_of(md)
        if have and have != want:
            stale.append((md.parent.name, have, want))
    return stale


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else str(PKG / "examples" / "expected")
    stale = check(root)
    if stale:
        print("DRIFT: %d skill(s) behind uber-standard VERSION %s" % (len(stale), current_version()))
        for name, have, want in stale:
            print("  - %s: baked %s, current %s (regenerate)" % (name, have, want))
        return 1
    print("DRIFT: none - all scanned skills match uber-standard VERSION %s" % current_version())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
