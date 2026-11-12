import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent


def test_ready(tmp_path):
    (tmp_path / "api.yaml").write_text("openapi: 3.0.0\n")
    r = subprocess.run([sys.executable, str(PKG / "scripts/preflight.py"), str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 0 and "READY" in r.stdout


def test_bad_json(tmp_path):
    (tmp_path / "x.json").write_text("{bad")
    r = subprocess.run([sys.executable, str(PKG / "scripts/preflight.py"), str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 1 and "NOT READY" in r.stdout
