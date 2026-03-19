"""Tests for LinkedIn content extractor."""

from unittest.mock import Mock, patch

import pytest

from src.domain.content_ingestion.extractors import LinkedInExtractor
from src.domain.content_ingestion.models import ExtractedContent


class TestLinkedInExtractor:
    """Test suite for LinkedInExtractor."""

    @pytest.fixture
    def extractor(self):
        """Create a LinkedInExtractor instance."""
        return LinkedInExtractor()

    def test_is_linkedin_url_valid(self, extractor):
        """Test recognition of valid LinkedIn URLs."""
        assert extractor._is_linkedin_url("https://www.linkedin.com/in/john-doe")
        assert extractor._is_linkedin_url("https://linkedin.com/posts/123")
        assert extractor._is_linkedin_url("http://LinkedIn.com/article/123")

    def test_is_linkedin_url_invalid(self, extractor):
        """Test rejection of non-LinkedIn URLs."""
        assert not extractor._is_linkedin_url("https://twitter.com/user")
        assert not extractor._is_linkedin_url("https://medium.com/article")
        assert not extractor._is_linkedin_url("https://example.com")

    @patch("domain.content_ingestion.extractors.requests.Session.get")
    def test_extract_success(self, mock_get, extractor):
        """Test successful content extraction."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html>
            <head>
                <title>John Doe Profile</title>
                <meta property="og:title" content="John Doe - Software Engineer">
                <meta name="description" content="John Doe's professional profile">
                <meta property="og:image" content="https://example.com/image.jpg">
            </head>
            <body>
                <h1>John Doe</h1>
                <p>Software engineer with 10 years of experience</p>
            </body>
        </html>
        """
        mock_response.text = mock_response.content.decode()
        mock_get.return_value = mock_response

        # Execute
        result = extractor.extract("https://www.linkedin.com/in/john-doe")

        # Assert
        assert result is not None
        assert isinstance(result, ExtractedContent)
        assert result.url == "https://www.linkedin.com/in/john-doe"
        assert result.title == "John Doe - Software Engineer"
        assert "engineer" in result.text.lower()

    @patch("domain.content_ingestion.extractors.requests.Session.get")
    def test_extract_http_error(self, mock_get, extractor):
        """Test handling of HTTP errors."""
        mock_get.side_effect = Exception("Connection timeout")

        result = extractor.extract("https://www.linkedin.com/in/john-doe")

        assert result is None

    def test_extract_non_linkedin_url(self, extractor):
        """Test rejection of non-LinkedIn URLs."""
        result = extractor.extract("https://twitter.com/user")

        assert result is None

    def test_extract_title_from_og_tag(self, extractor):
        """Test title extraction from og:title meta tag."""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <head>
                <meta property="og:title" content="Profile Title">
                <title>Default Title</title>
            </head>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        title = extractor._extract_title(soup)

        assert title == "Profile Title"

    def test_extract_title_from_title_tag(self, extractor):
        """Test title extraction from title tag."""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <head>
                <title>Page Title</title>
            </head>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        title = extractor._extract_title(soup)

        assert title == "Page Title"

    def test_extract_metadata(self, extractor):
        """Test metadata extraction."""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <head>
                <meta name="description" content="Profile description">
                <meta property="og:image" content="https://example.com/image.jpg">
            </head>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = extractor._extract_metadata(soup)

        assert metadata["description"] == "Profile description"
        assert metadata["image"] == "https://example.com/image.jpg"

    def test_extract_text_content(self, extractor):
        """Test text content extraction."""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <body>
                <script>console.log('test')</script>
                <h1>Title</h1>
                <p>This is the content</p>
                <p>More content here</p>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        text = extractor._extract_text(soup)

        assert "Title" in text
        assert "This is the content" in text
        assert "console.log" not in text  # script should be removed

    def test_extract_text_truncation(self, extractor):
        """Test that long text is truncated."""
        from bs4 import BeautifulSoup

        long_content = "x" * 15000
        html = f"<html><body><p>{long_content}</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        text = extractor._extract_text(soup)

        assert len(text) == 10000
