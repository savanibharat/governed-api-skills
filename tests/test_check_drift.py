from pathlib import Path
from scripts import check_drift

PKG = Path(__file__).resolve().parent.parent


def test_example_not_stale():
    assert check_drift.check(PKG / "examples/expected") == []


def test_detects_stale(tmp_path):
    d = tmp_path / "old-skill"
    d.mkdir()
    (d / "SKILL.md").write_text(
        '---\nname: old-skill\ndescription: x\nmetadata:\n  uber_standard_version: "0.0.1"\n---\n# b\n')
    stale = check_drift.check(tmp_path)
    assert stale and stale[0][0] == "old-skill"
