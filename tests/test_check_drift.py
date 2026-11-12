import shutil
from pathlib import Path

from scripts import check_drift

PKG = Path(__file__).resolve().parent.parent


def test_example_clean():
    assert check_drift.check(PKG / "examples/expected") == []


def test_detects_stale(tmp_path):
    d = tmp_path / "old-skill"
    (d / "references").mkdir(parents=True)
    (d / "SKILL.md").write_text(
        '---\nname: old-skill\ndescription: x\nmetadata:\n  uber_standard_version: "0.0.1"\n---\n# b\n')
    shutil.copy(PKG / "uber-standard/injection-defense.md", d / "references/injection-defense.md")
    issues = check_drift.check(tmp_path)
    assert any(n == "old-skill" and "stale" in w for n, w in issues)


def test_detects_missing_stamp(tmp_path):
    d = tmp_path / "nostamp"
    (d / "references").mkdir(parents=True)
    (d / "SKILL.md").write_text("---\nname: nostamp\ndescription: d\n---\n# b\n")
    shutil.copy(PKG / "uber-standard/injection-defense.md", d / "references/injection-defense.md")
    issues = check_drift.check(tmp_path)
    assert any("missing uber_standard_version" in w for _, w in issues)


def test_detects_tampered_guard(tmp_path):
    d = tmp_path / "customer-api"
    shutil.copytree(PKG / "examples/expected/customer-api", d)
    (d / "references/injection-defense.md").write_text("JUNK - hand edited\n")
    issues = check_drift.check(tmp_path)
    assert any("hash mismatch" in w for _, w in issues)
