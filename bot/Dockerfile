FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./

# Install Python dependencies
RUN uv sync --no-editable

# Copy source code
COPY src ./src

CMD ["python", "-m", "src"]
