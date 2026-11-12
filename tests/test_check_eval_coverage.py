from pathlib import Path

import yaml
from scripts import check_eval_coverage

PKG = Path(__file__).resolve().parent.parent
E = PKG / "examples/expected/customer-api/evals/eval-suite.yaml"


def test_example_ok():
    assert check_eval_coverage.check(E) == []


def test_missing_negative(tmp_path):
    suite = yaml.safe_load(E.read_text())
    suite["evals"] = [e for e in suite["evals"] if e["category"] != "negative"]
    f = tmp_path / "s.yaml"
    f.write_text(yaml.safe_dump(suite))
    assert any("negative" in p for p in check_eval_coverage.check(f))
