#!/usr/bin/env python3
"""
scan_output.py - laundering tripwire (governed-api-skills).

Scans the UNTRUSTED inputs for instruction-like snippets, then checks whether any flagged snippet
appears VERBATIM in the generated skill. This catches copy-through, NOT paraphrase - so it is a
tripwire, not a defense. The real controls against laundering are traceability (every instruction
must trace to a source) and independent review.

Importable: check(skill_dir, inputs_dir) -> list[str] of problems (empty == ok).
Exit 0 = ok; exit 1 = possible laundering.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scan_untrusted_doc  # noqa: E402

TEXT_SUFFIXES = (".md", ".txt", ".yaml", ".yml", ".json")


def _skill_text(skill_dir) -> str:
    parts = []
    for p in Path(skill_dir).rglob("*"):
        if p.is_file() and p.suffix in TEXT_SUFFIXES:
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def check(skill_dir, inputs_dir) -> list:
    flagged = set()
    for p in Path(inputs_dir).rglob("*"):
        if p.is_file() and p.suffix in TEXT_SUFFIXES:
            for f in scan_untrusted_doc.scan(p.read_text(encoding="utf-8", errors="replace")):
                snip = f["text"].strip()
                if len(snip) >= 12:
                    flagged.add(snip)
    text = _skill_text(skill_dir)
    return ["flagged input text reproduced in the generated skill: %r" % s for s in sorted(flagged) if s in text]


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: scan_output.py <skill_dir> <inputs_dir>")
        return 2
    problems = check(sys.argv[1], sys.argv[2])
    if problems:
        print("OUTPUT SCAN: FAIL (possible laundering - verify against traceability and review)")
        for p in problems:
            print("  - " + p)
        return 1
    print("OUTPUT SCAN: OK (no flagged input text copied verbatim; paraphrase still needs traceability + review)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
