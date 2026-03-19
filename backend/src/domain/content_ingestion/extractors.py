"""LinkedIn content extractor service."""

import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup

from domain.content_ingestion.models import ExtractedContent

logger = logging.getLogger(__name__)


class LinkedInExtractor:
    """Extracts content from LinkedIn URLs."""

    def __init__(self):
        """Initialize the LinkedIn extractor."""
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
            }
        )

    def extract(self, url: str) -> Optional[ExtractedContent]:
        """
        Extract content from a LinkedIn URL.

        Args:
            url: LinkedIn URL to extract from

        Returns:
            ExtractedContent with parsed data or None if extraction fails
        """
        try:
            if not self._is_linkedin_url(url):
                logger.warning(f"URL is not a LinkedIn URL: {url}")
                return None

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            return self._parse_content(url, soup, response.text)

        except requests.RequestException as e:
            logger.error(f"Failed to fetch LinkedIn URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None

    def _is_linkedin_url(self, url: str) -> bool:
        """Check if URL is from LinkedIn."""
        return "linkedin.com" in url.lower()

    def _parse_content(self, url: str, soup: BeautifulSoup, html: str) -> ExtractedContent:
        """
        Parse LinkedIn HTML content.

        Args:
            url: The source URL
            soup: BeautifulSoup object with parsed HTML
            html: Raw HTML string

        Returns:
            ExtractedContent with extracted metadata
        """
        # Extract title from meta tags or page content
        title = self._extract_title(soup)

        # Extract author/profile name
        author = self._extract_author(soup)

        # Extract main text content
        text = self._extract_text(soup)

        # Extract metadata
        metadata = self._extract_metadata(soup)

        return ExtractedContent(
            url=url,
            title=title,
            author=author,
            text=text,
            html=html,
            metadata=metadata,
        )

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract title from page."""
        # Try meta og:title first
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"]

        # Try meta title
        meta_title = soup.find("meta", {"name": "title"})
        if meta_title and meta_title.get("content"):
            return meta_title["content"]

        # Try <title> tag
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text(strip=True)

        return None

    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract author/profile name from page."""
        # Look for profile name in common LinkedIn HTML patterns
        author_elem = soup.find("meta", {"name": "author"})
        if author_elem and author_elem.get("content"):
            return author_elem["content"]

        # Try to find name in og:url or similar
        # LinkedIn post URLs often contain the name
        return None

    def _extract_text(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main text content from page."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator=" ", strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        text = " ".join(lines)

        # Limit to reasonable length
        if len(text) > 10000:
            text = text[:10000]

        return text if text else None

    def _extract_metadata(self, soup: BeautifulSoup) -> dict:
        """Extract metadata from page."""
        metadata = {}

        # Extract description
        description = soup.find("meta", {"name": "description"})
        if description and description.get("content"):
            metadata["description"] = description["content"]

        # Extract og:description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            metadata["og_description"] = og_desc["content"]

        # Extract og:image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            metadata["image"] = og_image["content"]

        return metadata
