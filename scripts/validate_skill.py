#!/usr/bin/env python3
"""
validate_skill.py - mechanical conformance gate for generated skills (governed-api-skills).

Mirrors the open Agent Skills standard plus the platform rules. Run on every generated skill
BEFORE routing it; the result is the first line of the skill's evaluation evidence.
Exit 0 = valid; exit 1 = invalid (reasons listed); exit 2 = usage error.

Importable: check(skill_dir) -> list[str] of problems (empty == valid).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
RESERVED = ("claude", "anthropic")
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def check(skill_dir) -> list:
    skill_dir = Path(skill_dir).resolve()
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return ["SKILL.md not found in %s" % skill_dir]
    m = re.match(r"^---\n(.*?)\n---", md.read_text(encoding="utf-8"), re.DOTALL)
    if not m:
        return ["no YAML frontmatter"]
    try:
        import yaml
    except ImportError:
        return ["PyYAML required to validate frontmatter"]
    fm = yaml.safe_load(m.group(1))
    if not isinstance(fm, dict):
        return ["frontmatter must be a mapping"]

    problems = []
    extra = set(fm) - ALLOWED
    if extra:
        problems.append("disallowed frontmatter key(s): " + ", ".join(sorted(extra)))

    name = fm.get("name")
    if not isinstance(name, str) or not name:
        problems.append("name missing or not a string")
    else:
        if not NAME_RE.fullmatch(name):
            problems.append("name '%s' must be kebab-case with no edge or consecutive hyphens" % name)
        if len(name) > 64:
            problems.append("name too long (%d > 64)" % len(name))
        if any(w in name for w in RESERVED):
            problems.append("name contains a reserved word: " + name)
        if name != skill_dir.name:
            problems.append("name '%s' must match directory '%s'" % (name, skill_dir.name))

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        problems.append("description missing or empty")
    else:
        if "<" in desc or ">" in desc:
            problems.append("description must not contain angle brackets")
        if len(desc) > 1024:
            problems.append("description too long (%d > 1024)" % len(desc))

    comp = fm.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or len(comp) > 500):
        problems.append("compatibility must be a string of at most 500 characters")
    return problems


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_skill.py <skill_dir>")
        return 2
    d = Path(sys.argv[1])
    problems = check(d)
    if problems:
        print("INVALID:")
        for p in problems:
            print("  - " + p)
        return 1
    print("VALID: " + d.resolve().name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
