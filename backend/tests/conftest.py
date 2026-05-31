import pytest
from fastapi.testclient import TestClient

from app.config.settings import settings
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    frontend_dir = tmp_path / "frontend"
    frontend_dir.mkdir()
    (frontend_dir / "index.html").write_text("<html><body>test</body></html>", encoding="utf-8")

    monkeypatch.setattr(settings, "database_path", str(db_path))
    monkeypatch.setattr(settings, "frontend_dir", str(frontend_dir))

    with TestClient(app) as test_client:
        yield test_client
