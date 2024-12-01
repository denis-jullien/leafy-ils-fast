from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import create_db_and_tables
from backend.routers import book, family, member  # circulation
from backend.users import (
    auth_backend,
    auth_cookie_backend,
    current_active_user,
    fastapi_users,
)
from backend.models import User, UserCreate, UserRead, UserUpdate


@asynccontextmanager
async def startup(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=startup)

API_PREFIX = "/api/v1"

app.include_router(book.router, prefix=API_PREFIX)
app.include_router(family.router, prefix=API_PREFIX)
app.include_router(member.router, prefix=API_PREFIX)
# app.include_router(circulation.router, prefix=API_PREFIX)

# Auth

AUTH_PREFIX = "/auth"

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=AUTH_PREFIX + "/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_cookie_backend),
    prefix=AUTH_PREFIX + "/cookie",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=AUTH_PREFIX,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=AUTH_PREFIX,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=AUTH_PREFIX,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# Demo auth route
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello  {user.email}!"}


# Serve static frontend
app.mount(
    "/",
    StaticFiles(directory="frontend/build", html=True, check_dir=False),
    name="sveltekit",
)
