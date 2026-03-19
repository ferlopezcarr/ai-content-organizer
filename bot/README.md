# Telegram Bot

User-facing Telegram bot that communicates with the backend service.

## Responsibilities

- Parse user commands and inputs
- Call backend endpoints for content extraction, search, and Q&A
- Format responses and send them back to Telegram

## Key Components

- src/clients/backend_client.py: HTTP client to backend
- src/handlers/: command handlers
- src/bot.py: bot initialization and handler registration

## Common Commands

- /start
- /add <url>
- /ask <question>
- /search <query>
- /browse
- /history

## Prerequisites

- Python 3.12+
- uv (dependency manager)
- Telegram bot token from @BotFather

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
# Edit .env with your Telegram bot token and backend URL
```

### Run

```bash
source .venv/bin/activate
python -m src
```

Bot will start polling Telegram for messages.

Make sure the backend is running before testing bot commands.

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
docker build -t content-organizer-bot .
docker run -e TELEGRAM_BOT_TOKEN=... -e BACKEND_URL=... content-organizer-bot
```

## Bot Commands

- `/start` — Show help
- `/add <URL>` — Extract and save content from LinkedIn URL
- `/ask <question>` — Ask question about your knowledge base
- `/search <query>` — Search for content
- `/browse` — Browse by categories
- `/history` — Show chat history

## Documentation

- Common architecture: [docs/service_architecture.md](../docs/service_architecture.md)
- Common code conventions: [docs/code_conventions.md](../docs/code_conventions.md)
- Bot code conventions: [bot/docs/code_conventions.md](../bot/docs/code_conventions.md)
- Bot testing instructions: [bot/docs/running_tests.md](../bot/docs/running_tests.md)
