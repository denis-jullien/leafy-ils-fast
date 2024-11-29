import sys

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import create_db_and_tables
from backend.routers import book, family, member, circulation


@asynccontextmanager
async def startup(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=startup)

API_PREFIX = "/api/v1"

app.include_router(book.router, prefix=API_PREFIX)
app.include_router(family.router, prefix=API_PREFIX)
app.include_router(member.router, prefix=API_PREFIX)
app.include_router(circulation.router, prefix=API_PREFIX)

# Serve static frontend
app.mount("/", StaticFiles(directory="frontend/build",  html=True, check_dir=False), name="sveltekit")
