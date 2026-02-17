start:
	python -m src

venv:
	uv venv

venv-activate:
	source .venv/bin/activate

sync:
	uv sync

format:
	black src
	ruff check src --fix

lint:
	ruff check src
	pylint src

check:
	black --check src
	ruff check src

test:
	pytest tests

test-coverage:
	uv run pytest --cov=src --cov-report=term-missing --cov-report=html tests