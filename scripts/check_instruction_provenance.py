#!/usr/bin/env python3
"""
check_instruction_provenance.py - tripwire for untraced operations in a generated skill
(governed-api-skills).

Traceability is self-reported by the generator, so an instruction can be added to SKILL.md that is
never listed in traceability.yaml. This check compares the skill body against what the skill
actually DOCUMENTS: every HTTP operation (METHOD /path) that SKILL.md instructs must appear in the
skill's own endpoint references (references/*.md). An operation like "DELETE /customers" that is
not documented is flagged.

This is a TRIPWIRE, not full semantic provenance: it catches undocumented operations, not every
paraphrased instruction. The complete control is traceability + independent review.

Importable: check(skill_dir) -> list[str] of problems. Exit 0 = ok; exit 1 = problems.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

OP_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/[^\s`)'\"]*)")


def _ops(text: str) -> set:
    out = set()
    for m in OP_RE.finditer(text):
        out.add((m.group(1).upper(), m.group(2).rstrip(".,);:")))
    return out


def check(skill_dir) -> list:
    d = Path(skill_dir)
    skill_md = (d / "SKILL.md")
    instructed = _ops(skill_md.read_text(encoding="utf-8")) if skill_md.exists() else set()
    documented = set()
    refs = (d / "references")
    if refs.is_dir():
        for ref in refs.glob("*.md"):
            documented |= _ops(ref.read_text(encoding="utf-8"))
    undocumented = sorted(instructed - documented)
    return ["skill instructs an operation not documented in references/: %s %s" % (v, p)
            for v, p in undocumented]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_instruction_provenance.py <skill_dir>")
        return 2
    problems = check(sys.argv[1])
    if problems:
        print("INSTRUCTION PROVENANCE: FAIL (untraced operation - verify against sources and review)")
        for p in problems:
            print("  - " + p)
        return 1
    print("INSTRUCTION PROVENANCE: OK (every instructed operation is documented in references/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
