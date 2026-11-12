import shutil
from pathlib import Path

import yaml
from scripts import check_routing

PKG = Path(__file__).resolve().parent.parent


def test_good_config():
    assert check_routing.check(PKG / "configuration") == []


def test_unrouted_and_disabled(tmp_path):
    cfg = tmp_path / "configuration"
    cfg.mkdir()
    shutil.copy(PKG / "configuration/artifact-routing.yaml", cfg / "artifact-routing.yaml")
    topo = yaml.safe_load((PKG / "configuration/repository-topology.yaml").read_text())
    topo["routing"].pop("mcp_reference")
    topo["repositories"]["federation"]["enabled"] = False
    (cfg / "repository-topology.yaml").write_text(yaml.safe_dump(topo))
    probs = check_routing.check(cfg)
    assert any("UNROUTED" in p for p in probs)
    assert any("DISABLED" in p for p in probs)
