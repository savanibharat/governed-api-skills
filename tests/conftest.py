"""Put the package root on sys.path so tests can `import scripts.<module>`."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PKG_ROOT = ROOT  # convenience for tests that need the package path
