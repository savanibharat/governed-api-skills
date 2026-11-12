from pathlib import Path
from scripts import validate_skill

PKG = Path(__file__).resolve().parent.parent


def _skill(tmp, frontmatter, name="customer-api"):
    d = tmp / name
    d.mkdir()
    (d / "SKILL.md").write_text("---\n" + frontmatter + "\n---\n\n# body\n")
    return d


def test_valid_example():
    assert validate_skill.check(PKG / "examples/expected/customer-api") == []


def test_missing_skill_md(tmp_path):
    (tmp_path / "foo").mkdir()
    assert validate_skill.check(tmp_path / "foo")


def test_reserved_word(tmp_path):
    d = _skill(tmp_path, "name: claude-api\ndescription: x", "claude-api")
    assert any("reserved" in p for p in validate_skill.check(d))


def test_angle_brackets(tmp_path):
    d = _skill(tmp_path, "name: customer-api\ndescription: use <this>")
    assert any("angle" in p for p in validate_skill.check(d))


def test_extra_key(tmp_path):
    d = _skill(tmp_path, 'name: customer-api\ndescription: ok\nversion: "1"')
    assert any("disallowed" in p for p in validate_skill.check(d))


def test_name_dir_mismatch(tmp_path):
    d = _skill(tmp_path, "name: other-name\ndescription: ok", "customer-api")
    assert any("match directory" in p for p in validate_skill.check(d))
