"""Tests for content extraction API endpoint."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from domain.content_ingestion.models import ExtractedContent
from infrastructure.api.app import app

client = TestClient(app)


class TestContentExtractionAPI:
    """Test suite for content extraction API."""

    @patch("infrastructure.api.routes.content.linkedin_extractor.extract")
    def test_extract_linkedin_success(self, mock_extract):
        """Test successful LinkedIn content extraction."""
        mock_content = ExtractedContent(
            url="https://www.linkedin.com/posts/123",
            title="Test Post",
            author="John Doe",
            text="This is test content",
            metadata={"image": "https://example.com/image.jpg"},
        )
        mock_extract.return_value = mock_content

        response = client.post(
            "/content/extract", json={"url": "https://www.linkedin.com/posts/123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://www.linkedin.com/posts/123"
        assert data["title"] == "Test Post"
        assert data["author"] == "John Doe"

    def test_extract_unsupported_url(self):
        """Test rejection of unsupported URLs."""
        response = client.post("/content/extract", json={"url": "https://twitter.com/user"})

        assert response.status_code == 400
        data = response.json()
        assert "unsupported" in data["detail"].lower()

    @patch("infrastructure.api.routes.content.linkedin_extractor.extract")
    def test_extract_linkedin_failure(self, mock_extract):
        """Test handling of extraction failure."""
        mock_extract.return_value = None

        response = client.post(
            "/content/extract", json={"url": "https://www.linkedin.com/posts/123"}
        )

        assert response.status_code == 400
        data = response.json()
        assert "failed" in data["detail"].lower()

    def test_extract_invalid_url(self):
        """Test rejection of invalid URLs."""
        response = client.post("/content/extract", json={"url": "not-a-url"})

        assert response.status_code == 422  # Validation error

    def test_extract_missing_url(self):
        """Test rejection of request without URL."""
        response = client.post("/content/extract", json={})

        assert response.status_code == 422  # Validation error
