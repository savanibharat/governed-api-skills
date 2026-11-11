#!/usr/bin/env python3
"""
validate_skill.py - mechanical conformance gate for generated skills (governed-api-skills).

Mirrors the open Agent Skills standard plus the platform rules. Run on every generated skill
BEFORE routing it; the result is the first line of the skill's evaluation evidence.
Exit 0 = valid; exit 1 = invalid (reason printed); exit 2 = usage error.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
RESERVED = ("claude", "anthropic")
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def fail(msg: str):
    print("INVALID: " + msg)
    raise SystemExit(1)


def validate(skill_dir: Path):
    skill_dir = skill_dir.resolve()
    md = skill_dir / "SKILL.md"
    if not md.exists():
        fail("SKILL.md not found")
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        fail("no YAML frontmatter")
    try:
        import yaml
    except ImportError:
        fail("PyYAML required to validate frontmatter")
    fm = yaml.safe_load(m.group(1))
    if not isinstance(fm, dict):
        fail("frontmatter must be a mapping")

    extra = set(fm) - ALLOWED
    if extra:
        fail("disallowed frontmatter key(s): " + ", ".join(sorted(extra)))

    name = fm.get("name")
    if not isinstance(name, str) or not name:
        fail("name missing or not a string")
    if not NAME_RE.fullmatch(name):
        fail("name '%s' must be kebab-case with no edge or consecutive hyphens" % name)
    if len(name) > 64:
        fail("name too long (%d > 64)" % len(name))
    if any(w in name for w in RESERVED):
        fail("name contains a reserved word: " + name)
    if name != skill_dir.name:
        fail("name '%s' must match directory '%s'" % (name, skill_dir.name))

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        fail("description missing or empty")
    if "<" in desc or ">" in desc:
        fail("description must not contain angle brackets")
    if len(desc) > 1024:
        fail("description too long (%d > 1024)" % len(desc))

    comp = fm.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or len(comp) > 500):
        fail("compatibility must be a string of at most 500 characters")

    print("VALID: " + name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_skill.py <skill_dir>")
        raise SystemExit(2)
    validate(Path(sys.argv[1]))
