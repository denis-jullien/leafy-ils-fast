from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import book, family, member


@asynccontextmanager
async def startup(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=startup)

app.include_router(book.router)
app.include_router(family.router)
app.include_router(member.router)
