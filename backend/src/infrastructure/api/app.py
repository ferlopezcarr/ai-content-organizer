"""FastAPI application factory."""

from fastapi import FastAPI

from infrastructure.api.routes.content import router as content_router

app = FastAPI(
    title="AI Content Organizer Backend",
    description="Backend API for content organization with RAG",
    version="0.1.0",
)

# Include routers
app.include_router(content_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
