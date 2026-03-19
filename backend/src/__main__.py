"""Backend main entry point."""

import logging

import uvicorn

from config.logging_config import setup_logging
from config.settings import settings

logger = logging.getLogger(__name__)


def main():
    """Start the backend API server."""
    setup_logging()
    logger.info("Starting backend server on %s:%d", settings.backend_host, settings.backend_port)

    uvicorn.run(
        "infrastructure.api.app:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    main()
