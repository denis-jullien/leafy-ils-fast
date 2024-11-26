FROM python:3.13-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR /app

COPY ./pyproject.toml poetry.lock ./

RUN poetry install

FROM python:3.13-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv .venv/
COPY .. .

EXPOSE 8000

CMD ["/app/.venv/bin/fastapi", "run"]