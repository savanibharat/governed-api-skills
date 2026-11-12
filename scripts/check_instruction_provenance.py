#!/usr/bin/env python3
"""
check_instruction_provenance.py - tripwire for untraced operations (governed-api-skills).

Compares every HTTP operation the skill INSTRUCTS (in SKILL.md and its references) against the
operations DEFINED IN THE SOURCE OpenAPI SPEC - the ground truth, NOT the generator-written
references. Any instructed operation absent from the spec is flagged. This closes the evasion
where the generator also "documents" a bogus operation in its own references.

Case-insensitive; understands full URLs; normalizes path parameters (/customers/{id} == /customers/42).

TRIPWIRE, not full provenance: pure-prose instructions with no METHOD/path token (e.g. "delete the
customer record via the API") are not detected. The complete control is traceability + review.

Importable: check(skill_dir, openapi_path=None) -> list[str]. Exit 0 = ok; exit 1 = problems.
Usage: python check_instruction_provenance.py <skill_dir> [openapi.yaml]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import yaml

METHODS = ("get", "post", "put", "patch", "delete", "head", "options")
OP_RE = re.compile(r"\b(" + "|".join(METHODS) + r")\b\s+(\S+)", re.I)


def _path_of(token: str):
    token = token.strip().strip("`'\"").rstrip(".,);:")
    mu = re.match(r"https?://[^/]+(/\S*)", token, re.I)
    if mu:
        return mu.group(1)
    return token if token.startswith("/") else None


def _normalize(path: str) -> str:
    path = path.split("?")[0].split("#")[0]
    path = path.rstrip("/") or "/"
    segs = []
    for s in path.split("/"):
        if re.fullmatch(r"\{[^}]*\}", s) or re.fullmatch(r"\d+", s) or s.startswith(":"):
            segs.append("{}")
        else:
            segs.append(s)
    return "/".join(segs)


def _ops_from_text(text: str) -> set:
    ops = set()
    for m in OP_RE.finditer(text):
        p = _path_of(m.group(2))
        if p:
            ops.add((m.group(1).upper(), _normalize(p)))
    return ops


def _instructed(skill_dir: Path) -> set:
    text = ""
    if (skill_dir / "SKILL.md").exists():
        text += (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    refs = skill_dir / "references"
    if refs.is_dir():
        for r in refs.glob("*.md"):
            text += "\n" + r.read_text(encoding="utf-8")
    return _ops_from_text(text)


def _allowed_from_openapi(openapi_path: Path) -> set:
    spec = yaml.safe_load(Path(openapi_path).read_text(encoding="utf-8")) or {}
    ops = set()
    for path, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method in item:
            if str(method).lower() in METHODS:
                ops.add((str(method).upper(), _normalize(path)))
    return ops


def check(skill_dir, openapi_path=None) -> list:
    d = Path(skill_dir)
    instructed = _instructed(d)
    if openapi_path and Path(openapi_path).exists():
        allowed = _allowed_from_openapi(Path(openapi_path))
        source = "the OpenAPI spec"
    else:
        # Weak fallback when no spec is available: the skill's own references (generator-written).
        refs = d / "references"
        allowed = set()
        if refs.is_dir():
            for r in refs.glob("*.md"):
                allowed |= _ops_from_text(r.read_text(encoding="utf-8"))
        source = "references (no OpenAPI provided - weak check; pass the spec for the real gate)"
    undoc = sorted(instructed - allowed)
    return ["skill instructs an operation not defined in %s: %s %s" % (source, v, p) for v, p in undoc]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_instruction_provenance.py <skill_dir> [openapi.yaml]")
        return 2
    problems = check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    if problems:
        print("INSTRUCTION PROVENANCE: FAIL (untraced operation - verify against the spec and review)")
        for p in problems:
            print("  - " + p)
        return 1
    print("INSTRUCTION PROVENANCE: OK (every instructed operation is defined in the source spec)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
