# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS frontend-builder

WORKDIR /app/frontend/

COPY ./frontend/package*.json /app/frontend/

RUN npm install

COPY ./frontend/ /app/frontend/

#ARG VITE_API_URL=${VITE_API_URL}

RUN npm run build


FROM python:3.13-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR /app

COPY ./pyproject.toml poetry.lock ./

RUN poetry install

FROM python:3.13-slim-bookworm

WORKDIR /app

COPY --from=frontend-builder /app/frontend/build/ frontend/build/

COPY --from=builder /app/.venv .venv/

COPY .. .

EXPOSE 8000

CMD ["/app/.venv/bin/fastapi", "run"]