"""Smoke tests for the FastAPI application."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from backend.app.main import create_app


def test_health_endpoint():
    app = create_app()
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "counts" in data
