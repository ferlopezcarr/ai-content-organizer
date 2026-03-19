"""Content ingestion models."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExtractedContent:
    """Represents extracted content from a URL."""

    url: str
    title: Optional[str] = None
    author: Optional[str] = None
    text: Optional[str] = None
    html: Optional[str] = None
    metadata: dict = field(default_factory=dict)
