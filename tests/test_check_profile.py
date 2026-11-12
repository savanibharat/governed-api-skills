import shutil
from pathlib import Path

import yaml
from scripts import check_profile

PKG = Path(__file__).resolve().parent.parent


def test_ok():
    assert check_profile.check(PKG / "configuration") == []


def test_silent_write_contradiction(tmp_path):
    cfg = tmp_path / "configuration"
    cfg.mkdir()
    for f in ("workspace-profile.yaml", "artifact-routing.yaml"):
        shutil.copy(PKG / "configuration" / f, cfg / f)
    topo = yaml.safe_load((PKG / "configuration/repository-topology.yaml").read_text())
    topo["repositories"]["federation"]["approval_required"] = False
    (cfg / "repository-topology.yaml").write_text(yaml.safe_dump(topo))
    assert check_profile.check(cfg)
