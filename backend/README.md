# Backend Service

FastAPI service providing content management, knowledge base, and RAG APIs.

## Prerequisites

- Python 3.12+
- uv (dependency manager)
- Docker (for local PostgreSQL)
- LM Studio running at http://192.168.1.152:1234

## Local Development (venv + uv)

### Setup

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv sync

# Copy environment file
cp .env.example .env
```

### Start PostgreSQL (docker-compose)

```bash
docker-compose up -d postgres
# PostgreSQL available at localhost:5432
```

### Run Backend

```bash
source .venv/bin/activate
python -m src
```

API docs available at http://localhost:8000/docs

### Stop PostgreSQL

```bash
docker-compose down
# Or clean with: docker-compose down -v
```

### Testing

```bash
source .venv/bin/activate
pytest
pytest --cov=src
```

### Code Quality

```bash
source .venv/bin/activate
ruff check src tests
black src tests
```

## Cloud Deployment (Docker)

The `Dockerfile` is provided for deploying to cloud platforms (AWS ECS, Google Cloud Run, etc.).

Build and run:
```bash
docker build -t content-organizer-backend .
docker run -e DATABASE_URL=... -e LLM_API_URL=... -p 8000:8000 content-organizer-backend
```

## Documentation

- Common architecture: [docs/service_architecture.md](../docs/service_architecture.md)
- Common code conventions: [docs/code_conventions.md](../docs/code_conventions.md)
- Backend overview: [backend/docs/project_overview.md](../backend/docs/project_overview.md)
- Backend build guide: [backend/docs/building_the_project.md](../backend/docs/building_the_project.md)
- Backend API reference: [backend/docs/api_endpoints.md](../backend/docs/api_endpoints.md)

## API Endpoints

- `POST /api/{user_id}/content/extract` — Extract content from URL
- `POST /api/{user_id}/content/confirm` — Save content with categories
- `POST /api/{user_id}/chat/ask` — Ask question about knowledge base
- `GET /api/{user_id}/knowledge/search?q=...` — Search content
- `GET /api/{user_id}/chat/history` — Get chat history
