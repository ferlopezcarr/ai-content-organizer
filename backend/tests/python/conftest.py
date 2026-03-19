"""Backend test configuration."""

import sys
from pathlib import Path

import pytest

SRC_PATH = Path(__file__).resolve().parents[2] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    """Ensure required environment variables are set for tests."""
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
