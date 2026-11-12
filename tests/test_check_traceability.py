from pathlib import Path

import yaml
from scripts import check_traceability

PKG = Path(__file__).resolve().parent.parent
E = PKG / "examples/expected/customer-api"


def test_example_ok():
    assert check_traceability.check(E / "traceability.yaml", E / "evals/eval-suite.yaml") == []


def test_unknown_with_instruction(tmp_path):
    d = yaml.safe_load((E / "traceability.yaml").read_text())
    d["requirements"][-1]["instruction"] = "x"
    f = tmp_path / "t.yaml"
    f.write_text(yaml.safe_dump(d))
    assert any("must not carry an instruction" in p
               for p in check_traceability.check(f, E / "evals/eval-suite.yaml"))


def test_missing_source(tmp_path):
    d = yaml.safe_load((E / "traceability.yaml").read_text())
    d["requirements"][0]["source"] = "none"
    f = tmp_path / "t.yaml"
    f.write_text(yaml.safe_dump(d))
    assert any("no source" in p for p in check_traceability.check(f))
