#!/usr/bin/env python3
"""
check_traceability.py - mechanical traceability gate (governed-api-skills).

Verifies that every IMPLEMENTED requirement has a real source and an eval that actually exists,
and that an 'unknown' requirement carries NO instruction but DOES record an open_question. This
is the check RUN.md step 5 claims but nothing enforced before.

Importable: check(traceability_path, eval_suite_path=None) -> list[str] of problems.
Exit 0 = ok; exit 1 = problems; exit 2 = usage.
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

PKG = Path(__file__).resolve().parent.parent


def _load(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def check(trace_path, eval_suite_path=None) -> list:
    problems = []
    doc = _load(trace_path)
    sch = _load(PKG / "schemas" / "traceability.schema.yaml")
    for e in list(Draft202012Validator(sch).iter_errors(doc))[:5]:
        problems.append("schema: %s" % e.message)

    eval_ids = set()
    if eval_suite_path and Path(eval_suite_path).exists():
        eval_ids = {ev.get("test_id") for ev in (_load(eval_suite_path).get("evals") or [])}

    for req in (doc.get("requirements") or []):
        rid = req.get("id", "?")
        prov = req.get("provenance")
        src = (req.get("source") or "").strip().lower()
        if prov == "unknown":
            if req.get("instruction") not in (None, ""):
                problems.append("%s: 'unknown' provenance must not carry an instruction" % rid)
            if not req.get("open_question"):
                problems.append("%s: 'unknown' provenance must record an open_question" % rid)
        else:
            if not src or src == "none":
                problems.append("%s: implemented requirement has no source (provenance=%s)" % (rid, prov))
            if req.get("instruction") in (None, ""):
                problems.append("%s: implemented requirement has no instruction" % rid)
            ev = req.get("eval")
            if not ev:
                problems.append("%s: implemented requirement has no eval" % rid)
            elif eval_ids and ev not in eval_ids:
                problems.append("%s: eval '%s' not found in the eval suite" % (rid, ev))
    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_traceability.py <traceability.yaml> [eval-suite.yaml]")
        return 2
    problems = check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    if problems:
        print("TRACEABILITY: FAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("TRACEABILITY: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
