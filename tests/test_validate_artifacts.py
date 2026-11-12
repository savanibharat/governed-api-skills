from pathlib import Path
from scripts import validate_artifacts

PKG = Path(__file__).resolve().parent.parent


def test_example_ok():
    assert validate_artifacts.check(PKG / "examples/expected/customer-api") == []


def test_bad_mapping(tmp_path):
    (tmp_path / "presentation-mapping.yaml").write_text("title: 1\n")  # title must be a string; sections missing
    assert validate_artifacts.check(tmp_path)
