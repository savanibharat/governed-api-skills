#!/usr/bin/env python3
"""
validate_artifacts.py - schema-validate a generated skill's artifacts (governed-api-skills).

Enforces the package's own schemas/ against the evals, presentation mapping, registration, and
traceability that a generated skill ships. This is what turns schemas/ from documentation into a
gate. Run it at generate / validate / route time.

Importable: check(skill_dir) -> list[str] of problems (empty == ok).
Exit 0 = ok; exit 1 = problems; exit 2 = usage.
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

PKG = Path(__file__).resolve().parent.parent
SCH = PKG / "schemas"


def _load(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def _validate(schema_file, doc, label, problems):
    for e in list(Draft202012Validator(_load(SCH / schema_file)).iter_errors(doc))[:5]:
        problems.append("%s: %s" % (label, e.message))


def check(skill_dir) -> list:
    d = Path(skill_dir)
    problems = []
    pm = d / "presentation-mapping.yaml"
    if pm.exists():
        _validate("presentation-mapping.schema.yaml", _load(pm), "presentation-mapping", problems)
    reg = d / "registration.yaml"
    if reg.exists():
        _validate("skill-registration.schema.yaml", _load(reg), "registration", problems)
    tr = d / "traceability.yaml"
    if tr.exists():
        _validate("traceability.schema.yaml", _load(tr), "traceability", problems)
    suites = sorted((d / "evals").glob("*.yaml")) if (d / "evals").is_dir() else []
    for s in suites:
        for ev in (_load(s).get("evals") or []):
            _validate("evaluation.schema.yaml", ev, "%s:%s" % (s.name, ev.get("test_id")), problems)
    if not (pm.exists() or reg.exists() or tr.exists() or suites):
        problems.append("no artifacts found to validate in %s" % d)
    return problems


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_artifacts.py <skill_dir>")
        return 2
    problems = check(sys.argv[1])
    if problems:
        print("ARTIFACTS: FAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("ARTIFACTS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
