import importlib.util
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


def _rm():
    spec = importlib.util.spec_from_file_location("render_markdown", str(PKG / "uber-standard" / "render_markdown.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


rm = _rm()


def test_get_path():
    assert rm.get_path({"a": {"b": 1}}, "a.b") == 1
    assert rm.get_path({"items": [{"x": 9}]}, "items.0.x") == 9
    assert rm.get_path({"a": 1}, "missing") is None


def test_sanitize_truncates_name():
    s = rm.sanitize("x" * 100, is_name=True)
    assert len(s) <= 64 and s.endswith("…")


def test_sanitize_redacts():
    assert rm.sanitize("anything", redact=True) == "[redacted]"


def test_sanitize_strips_zero_width_and_escapes_pipe():
    assert "​" not in rm.sanitize("a​b")
    assert rm.sanitize("a|b") == "a\\|b"


def test_render_redacts_secret_in_table():
    data = {"rows": [{"id": 1, "api_key": "sk-x", "name": "Acme"}]}
    mp = {"title": "T", "sections": [{"heading": "R", "kind": "table", "source": "rows",
          "columns": [{"label": "ID", "path": "id"}, {"label": "Key", "path": "api_key"},
                      {"label": "Name", "path": "name", "name": True}]}]}
    out = rm.render(mp, data)
    assert "sk-x" not in out and "[redacted]" in out and "Acme" in out


def test_render_is_deterministic():
    mp = {"title": "T", "sections": [{"kind": "fields", "source": "", "fields": [{"label": "A", "path": "a"}]}]}
    d = {"a": "val"}
    assert rm.render(mp, d) == rm.render(mp, d)
