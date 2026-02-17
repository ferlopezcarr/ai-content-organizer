# ai-content-organizer

## Requirements

- Python 3.12
- `venv` (or another virtualenv manager)

## Installation

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
uv sync
```

## Formatting & linting

This project uses `black` and `ruff`. Configuration lives in `pyproject.toml`.

- Format code:

```bash
make format
```

- Lint (check):

```bash
make lint
```

## Tests

Run the test suite with:

```bash
make test
# or
pytest tests
```

## Running the script

```bash
python -m src
```
