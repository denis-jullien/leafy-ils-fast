from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import xml.etree.ElementTree as ET
from io import StringIO

from pydantic import BaseModel
from rdflib import Graph, RDF
from app.books import Book, clean_isbn
from devtools import pprint, debug
import httpx


router = APIRouter(
    prefix="/book",
    tags=["book"],
)

templates = Jinja2Templates(directory='./templates')

async def isbn2book(in_isbn: str)-> Book:
    async with httpx.AsyncClient() as client:

        isbn = clean_isbn(in_isbn)  # "978-2013944762"
        r = await client.get(f'https://www.sudoc.fr/services/isbn2ppn/{isbn}')
        # print(r.text)

        root = ET.fromstring(r.text)
        # print(root.tag)

        if root.find('error') != None:
            print("return isbn2ppn Error !")

        x = root.find('query/resultNoHolding')
        if x == None:
            x = root.find('query/result')

        ppn = x.find('ppn').text
        print(f"Got PPN: {ppn}")

        r = await client.get(f'https://www.sudoc.fr/{ppn}.rdf')
        # print(r.text)

        # Create a Graph
        g = Graph()

        # Parse in an RDF file hosted on the Internet
        g.parse(StringIO(r.text), format='application/rdf+xml')

        knows_query3 = """
        select ?book ?title ?abstract ?date ?publisher ?format where {
            ?book a bibo:Book . 
            ?book dc:title ?title .
            OPTIONAL { ?book dcterms:abstract ?abstract }
            ?book dc:date ?date .
            ?book dc:publisher ?publisher .
            ?book dc:format ?format .
        }"""

        qres = g.query(knows_query3)
        for row in qres:
            debug(row)
            print(f"{row.book} knows {row.title}")

            book = Book(title=row.title,
                        abstract=row.abstract or "",
                        publication_year=row.date,
                        publisher=row.publisher,
                        author=row.title,
                        format=row.format,
                        language='fr',
                        isbn13=isbn,
                        )

        debug(book)

    return book






# Example isbn
# 978-2013944762
# 9782253067900
# 9782377940820
# 9782070438617
@router.get("/notice")
async def hello_func(in_isbn: str):
    boo = await isbn2book(in_isbn)
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

