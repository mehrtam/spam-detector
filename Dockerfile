# Change FROM python:3.11-slim to:
FROM python:3.13-slim

WORKDIR /app

# Disable virtualenv creation inside Docker (recommended)
ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root --no-interaction --no-ansi

COPY src/ ./src/
COPY models/ ./models/
COPY config/ ./config/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]