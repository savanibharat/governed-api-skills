#!/usr/bin/env python3
"""
scan_untrusted_doc.py - build-time injection-scan ASSIST (governed-api-skills).

Flags instruction-like content in an ingested document so it can be treated as DATA, not
instructions.

ADVISORY TRIPWIRE, NOT A DEFENSE. It normalizes Unicode (NFKC) and matches known patterns, but
rephrasing, novel wording, or other languages can evade it. The real defense is the treat-as-data
discipline (uber-standard/injection-defense.md) and the deterministic renderer - not this scanner.
It surfaces findings for review and never blocks or acts on them. Feed already-extracted text
(.md / .txt); extract PDF text first.

Usage:
    python scan_untrusted_doc.py FILE [--json]

Exit code is always 0; the finding count is printed.
"""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path

PATTERNS = [
    ("instruction-override", r"\b(ignore|disregard|forget)\b.{0,40}\b(instruction|instructions|rules|prompt)\b"),
    ("role-injection", r"(^|\s)(system|assistant|developer)\s*:"),
    ("prompt-extraction", r"\breveal\b.{0,25}\bprompt\b|\bprint\b.{0,25}\b(instructions|system)\b"),
    ("act-as", r"\b(you are now|act as|pretend to be|roleplay as|from now on)\b"),
    ("privilege", r"\b(grant|enable|allow|escalate)\b.{0,40}\b(admin|root|scope|privilege|access)\b"),
    ("exfiltration", r"\b(exfiltrat\w*|send|post|email|upload|leak)\b.{0,40}(https?://|@|elsewhere)"),
    ("disable-safety", r"\b(disable|turn off|bypass|skip|override)\b.{0,25}\b(safety|guard\w*|validation|check|filter|rule)\b"),
    ("imperative", r"\byou must\b|\byou should always\b|\bdo not tell\b|\bnever tell\b|\bwithout telling\b"),
    ("hidden-comment", r"<!--.*?-->"),
]
COMPILED = [(name, re.compile(p, re.I)) for name, p in PATTERNS]


def scan(text: str):
    findings = []
    for i, raw in enumerate(text.splitlines(), 1):
        line = unicodedata.normalize("NFKC", raw)  # fold homoglyph/compatibility forms first
        for name, rx in COMPILED:
            if rx.search(line):
                snippet = line.strip()
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                findings.append({"line": i, "type": name, "text": snippet})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Injection-scan assist for untrusted docs.")
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = Path(a.file).read_text(encoding="utf-8", errors="replace")
    findings = scan(text)
    if a.json:
        print(json.dumps({"file": a.file, "count": len(findings), "findings": findings}, indent=2))
    elif not findings:
        print("No injection indicators found in %s." % a.file)
    else:
        print("%d injection indicator(s) in %s - treat this content as DATA:" % (len(findings), a.file))
        for f in findings:
            print("  line %d: [%s] %s" % (f["line"], f["type"], f["text"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
