from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Response, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



from pydantic import BaseModel

from app.books import Book, isbn2book
from devtools import pprint, debug

router = APIRouter(
    prefix="/book",
    tags=["book"],
)

templates = Jinja2Templates(directory='./templates')


# Example isbn
# 978-2013944762
# 9782253067900
# 9782377940820
# 9782070438617
# 9780738531366
@router.get("/notice")
async def hello_func(in_isbn: str, response: Response):
    boo = await isbn2book(in_isbn)
    if boo is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return boo

@router.post("/notice")
async def hello_func_post(in_isbn: str):
    boo = await isbn2book(in_isbn)
    if boo is None:
        raise HTTPException(status_code=400, detail="Item not found")
    return boo

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/add", response_class=HTMLResponse)
async def book_add(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("book_add.html", context)

@router.post("/add", response_class=HTMLResponse)
async def book_add( request: Request, book: Book):

    debug(book)

    context = {
         "request": request,
    }
    return templates.TemplateResponse("book_add.html", context)

class IsbnInput(BaseModel):
    in_isbn: str


@router.post("/getinfo", response_class=HTMLResponse)
async def book_add_post(request: Request, item: IsbnInput):

    debug(item)

    context = {
        "request": request,
        "book": await isbn2book(item.in_isbn)
    }
    return templates.TemplateResponse("book_add.html", context)

@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}

