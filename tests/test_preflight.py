import shutil
from pathlib import Path

import yaml
from scripts import preflight

PKG = Path(__file__).resolve().parent.parent


def _cfg(tmp, repo_exists=True):
    cfg = tmp / "configuration"
    cfg.mkdir()
    for f in ("artifact-routing.yaml", "workspace-profile.yaml"):
        shutil.copy(PKG / "configuration" / f, cfg / f)
    topo = yaml.safe_load((PKG / "configuration/repository-topology.yaml").read_text())
    base = tmp / "repos"
    base.mkdir()
    for repo in topo["repositories"].values():
        target = base / Path(repo["path"]).name
        if repo_exists:
            target.mkdir(parents=True, exist_ok=True)
        repo["path"] = str(target)  # absolute; exists iff repo_exists
    (cfg / "repository-topology.yaml").write_text(yaml.safe_dump(topo))
    return cfg


def test_ready(tmp_path):
    cfg = _cfg(tmp_path, True)
    inp = tmp_path / "inp"
    inp.mkdir()
    (inp / "api.yaml").write_text("openapi: 3.0.0\npaths: {}\n")
    problems, _ = preflight.check(inp, cfg)
    assert problems == []


def test_missing_enabled_repo(tmp_path):
    cfg = _cfg(tmp_path, False)
    inp = tmp_path / "inp"
    inp.mkdir()
    problems, _ = preflight.check(inp, cfg)
    assert any("does not exist" in p for p in problems)


def test_bad_yaml_input(tmp_path):
    cfg = _cfg(tmp_path, True)
    inp = tmp_path / "inp"
    inp.mkdir()
    (inp / "x.yaml").write_text("a: [unclosed\n")
    problems, _ = preflight.check(inp, cfg)
    assert any("invalid" in p for p in problems)


def test_bad_json_input(tmp_path):
    cfg = _cfg(tmp_path, True)
    inp = tmp_path / "inp"
    inp.mkdir()
    (inp / "x.json").write_text("{bad")
    problems, _ = preflight.check(inp, cfg)
    assert any("invalid" in p for p in problems)
