#!/usr/bin/env python3
"""
check_eval_coverage.py - enforce the eval coverage policy on a skill's eval suite
(governed-api-skills).

Reads configuration/evaluation-policy.yaml `coverage`: minimum negative and regression tests, and
required categories. This replaces the previous "only a functional pass rate" bar.

Importable: check(eval_suite_path, policy_path=None) -> list[str] of problems.
Exit 0 = ok; exit 1 = problems.
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

PKG = Path(__file__).resolve().parent.parent


def _load(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def check(eval_suite_path, policy_path=None) -> list:
    policy = _load(policy_path or (PKG / "configuration" / "evaluation-policy.yaml")) or {}
    cov = policy.get("coverage", {})
    suite = _load(eval_suite_path) or {}
    counts = {}
    for ev in (suite.get("evals") or []):
        counts[ev.get("category")] = counts.get(ev.get("category"), 0) + 1
    problems = []
    if counts.get("negative", 0) < cov.get("min_negative_tests", 0):
        problems.append("needs >= %d negative tests, has %d" % (cov.get("min_negative_tests", 0), counts.get("negative", 0)))
    if counts.get("regression", 0) < cov.get("min_regression_tests", 0):
        problems.append("needs >= %d regression tests, has %d" % (cov.get("min_regression_tests", 0), counts.get("regression", 0)))
    for cat in (cov.get("require_categories") or []):
        if counts.get(cat, 0) < 1:
            problems.append("missing required eval category: %s" % cat)
    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_eval_coverage.py <eval-suite.yaml> [policy.yaml]")
        return 2
    problems = check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    if problems:
        print("EVAL COVERAGE: FAIL")
        for p in problems:
            print("  - " + p)
        return 1
    print("EVAL COVERAGE: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
