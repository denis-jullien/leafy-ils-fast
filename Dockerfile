# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS frontend-builder

WORKDIR /app/frontend/

COPY ./frontend/package*.json /app/frontend/

RUN npm install

COPY ./frontend/ /app/frontend/

#ARG VITE_API_URL=${VITE_API_URL}

RUN npm run build


FROM python:3.13.0-alpine3.20 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR /app

RUN python -m venv .venv
#ENV PATH="/app/.venv/bin:$PATH"

COPY ./requirements.txt ./
RUN /app/.venv/bin/pip install -r requirements.txt

FROM python:3.13.0-alpine3.20

WORKDIR /app

COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
# Copy the possible LiteFS configurations.
ADD fly-io-config/etc/litefs.yml /etc/litefs.yml

# Setup our environment to include FUSE & SQLite. We install ca-certificates
# so we can communicate with the Consul server over HTTPS. cURL is added so
# we can call our HTTP endpoints for debugging.
RUN apk add bash fuse3 sqlite ca-certificates curl
#RUN apk add ca-certificates fuse3 sqlite

COPY --from=frontend-builder /app/frontend/build/ frontend/build/

COPY --from=builder /app/.venv /app/.venv/

COPY ./backend/ /app/backend/

EXPOSE 8000

CMD ["/app/.venv/bin/fastapi", "run", "backend/main.py"]
#ENTRYPOINT litefs mount