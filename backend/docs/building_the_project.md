# Building the Backend

This guide focuses on setting up and running the backend service.

## Prerequisites

- Python 3.12+
- uv (dependency manager)
- Docker (for local PostgreSQL)
- LM Studio running at http://192.168.1.152:1234

## Initial Setup

From the repository root:

```bash
make setup
```

This creates backend and bot virtual environments, installs dependencies, and prepares local environment files.

## Configure Environment

Update backend settings in backend/.env based on backend/.env.example:

```env
LLM_API_URL=http://192.168.1.152:1234
LLM_MODEL=mistral
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/content_organizer
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Start Dependencies

```bash
make db-start
```

PostgreSQL will be available at localhost:5432.

## Run the Backend

```bash
make start-backend
```

FastAPI docs will be available at http://localhost:8000/docs.

## Backend Development Commands

```bash
cd backend
source .venv/bin/activate

python -m src          # Run
make test              # Tests
make lint              # Lint
make format            # Format
```
