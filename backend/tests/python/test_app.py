"""FastAPI app tests."""

from fastapi.testclient import TestClient

from src.infrastructure.api.app import app


def test_health_check():
    """Health endpoint should return healthy status."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
