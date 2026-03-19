"""Content extraction API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from domain.content_ingestion.extractors import LinkedInExtractor

router = APIRouter(prefix="/content", tags=["content"])

# Initialize extractor
linkedin_extractor = LinkedInExtractor()


class ContentExtractionRequest(BaseModel):
    """Request model for content extraction."""

    url: HttpUrl


class ContentExtractionResponse(BaseModel):
    """Response model for extracted content."""

    url: str
    title: str | None = None
    author: str | None = None
    text: str | None = None
    metadata: dict = {}


@router.post("/extract", response_model=ContentExtractionResponse)
async def extract_content(request: ContentExtractionRequest):
    """
    Extract content from a URL.

    Currently supports LinkedIn URLs. Other sources can be added in the future.

    Args:
        request: ContentExtractionRequest with URL to extract

    Returns:
        ContentExtractionResponse with extracted content

    Raises:
        HTTPException: If extraction fails or URL is not supported
    """
    url = str(request.url)

    # Route to appropriate extractor based on URL
    if "linkedin.com" in url:
        result = linkedin_extractor.extract(url)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported URL. Currently only LinkedIn URLs are supported.",
        )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Failed to extract content from the provided URL.",
        )

    return ContentExtractionResponse(
        url=result.url,
        title=result.title,
        author=result.author,
        text=result.text,
        metadata=result.metadata,
    )
