import importlib
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def set_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set required environment variables for backend.settings."""
    # Ensure project root is on sys.path for `import backend`
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    monkeypatch.setenv("DMR_BASE_URL", "http://localhost:8001")
    monkeypatch.setenv("DMR_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_ID", "ai/test-model:latest")
    # API_BASE_URL is optional for backend


@pytest.fixture()
def client(set_env: None) -> TestClient:
    """Create a TestClient with a fresh settings cache."""
    # Ensure settings cache is cleared before importing app
    from backend import settings as backend_settings

    backend_settings.get_settings.cache_clear()
    # Import or reload app after env is set
    module = importlib.import_module("backend.main")
    importlib.reload(module)
    app = module.app
    return TestClient(app)
