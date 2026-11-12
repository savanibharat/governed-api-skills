#!/usr/bin/env python3
"""
check_drift.py - detect generated skills whose baked uber guards are stale, unstamped, or TAMPERED
(governed-api-skills).

A generated skill is one that carries baked guards (references/injection-defense.md). For each:
- it MUST carry metadata.uber_standard_version (else: unstamped);
- the stamp MUST equal the current uber-standard/VERSION (else: stale);
- when the stamp is current, each baked guard FILE must hash-match the current uber-standard file
  (else: modified / missing). This catches hand-edits that a version-only check would miss.

Importable: check(skills_root) -> list of (name, issue). Exit 0 = clean; exit 1 = issues.
Usage: python check_drift.py [skills_root]   # defaults to the bundled examples/expected
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parent.parent
GUARD_FILES = {   # baked path inside a skill -> source file in uber-standard/
    "references/injection-defense.md": "injection-defense.md",
    "references/output-sanitization.md": "output-sanitization.md",
    "references/naming-validation.md": "naming-validation.md",
    "scripts/render_markdown.py": "render_markdown.py",
}


def current_version() -> str:
    return (PKG / "uber-standard" / "VERSION").read_text(encoding="utf-8").strip()


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _version_of(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    return (fm.get("metadata") or {}).get("uber_standard_version")


def check(skills_root) -> list:
    want = current_version()
    issues = []
    for md in sorted(Path(skills_root).rglob("SKILL.md")):
        d = md.parent
        has_guards = (d / "references" / "injection-defense.md").exists()
        have = _version_of(md)
        if not has_guards and not have:
            continue  # not a generated skill (e.g. the factory itself)
        name = d.name
        if has_guards and not have:
            issues.append((name, "missing uber_standard_version stamp"))
            continue
        if have != want:
            issues.append((name, "stale: baked %s, current %s (regenerate)" % (have, want)))
            continue
        # stamp is current: the baked guard files must actually match the current uber standard
        for baked_rel, src_name in GUARD_FILES.items():
            baked = d / baked_rel
            src = PKG / "uber-standard" / src_name
            if not baked.exists():
                issues.append((name, "baked guard missing: %s" % baked_rel))
            elif _sha(baked) != _sha(src):
                issues.append((name, "baked guard modified (hash mismatch): %s" % baked_rel))
    return issues


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else str(PKG / "examples" / "expected")
    issues = check(root)
    if issues:
        print("DRIFT: %d issue(s) vs uber-standard VERSION %s" % (len(issues), current_version()))
        for name, why in issues:
            print("  - %s: %s" % (name, why))
        return 1
    print("DRIFT: none - scanned skills match uber-standard VERSION %s (stamp + file hashes)" % current_version())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
