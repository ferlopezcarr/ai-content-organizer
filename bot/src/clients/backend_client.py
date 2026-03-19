"""Backend API client."""

import httpx

from config.settings import settings


class BackendClient:
    """Client for backend API calls."""

    def __init__(self):
        """Initialize backend client."""
        self.base_url = settings.backend_url

    async def extract_content(self, url: str):
        """Extract content from URL.

        Args:
            url: The URL to extract content from (currently supports LinkedIn)

        Returns:
            dict: Extracted content with url, title, author, text, and metadata

        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/content/extract",
                json={"url": url},
            )
            response.raise_for_status()
            return response.json()

    async def confirm_content(self, user_id: int, content_data: dict):
        """Confirm and save content (TODO: backend endpoint not yet implemented)."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/{user_id}/content/confirm",
                json=content_data,
            )
            response.raise_for_status()
            return response.json()

    async def ask_question(self, user_id: int, query: str):
        """Ask a question about knowledge base (TODO: backend endpoint not yet implemented)."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/{user_id}/chat/ask",
                json={"query": query},
            )
            response.raise_for_status()
            return response.json()

    async def search_knowledge(self, user_id: int, query: str, limit: int = 5):
        """Search knowledge base (TODO: backend endpoint not yet implemented)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/{user_id}/knowledge/search",
                params={"q": query, "limit": limit},
            )
            response.raise_for_status()
            return response.json()


backend_client = BackendClient()
