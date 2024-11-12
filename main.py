from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, auth_cookie_backend, current_active_user, fastapi_users
from app.admin import admin

import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)  

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_auth_router(auth_cookie_backend), prefix="/auth/cookie", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


async def isbn2book(in_isbn: str):
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

def booklist():
    return [
        Book(
            title="Je t'aimerai toujours, quoi qu'il arrive",
            author="Debi Gliori  ; [adaptation française de Marie-France Floury]",
            publisher='Paris : Gautier-Languereau , impr. 2014',
            isbn13=9782013944762,
            publication_year=2014,
            abstract='',
            language='fr',
            format='1 vol. (non paginé [30] p.) : ill. en coul., couv. ill. en coul. ; 18 cm',
            url=None
        ),
        Book(
            title='La végétarienne',
            author='Han Kang  ; traduit du coréen par Jeong Eun-Jin & Jacques Batilliot',
            publisher='Paris : le Livre de poche , DL 2016',
            isbn13=9782253067900,
            publication_year=2016,
            abstract='',
            language='fr',
            format='1 volume (211 pages) : couverture illustrée ; 18 cm',
            url=None,
        ) ,
        Book(
            title='Moi, François le Français',
            author='Georges Piombo',
            publisher='Paris : Éditions Libre & Solidaire , 2022',
            isbn13=9782377940820,
            publication_year=2022,
            abstract=(
                "La vie est une aventure. Ma mère et mon père, une histoire d'amour au-dessus de tout. Il l'a enlevée, ils"
                " ont fait la « carrossela », sont partis sans se retourner, ont quitté le pays, la famiglia. Quand l'amou"
                "r est le plus fort, l'enfant paraît. L'enfant c'est moi, François le Français. Je veux être le meilleur F"
                "rançais possible, servir mon pays, m'émanciper ailleurs. D'autant plus qu'elle ne m'aime plus, ses soleil"
                "s ne brillent plus pour moi. Je m'en vais traverser la guerre, le siècle. Je veux devenir riche ; riche d"
                "e quoi ? La vie est une aventure, rencontrer l'autre est une jouissance."
            ),
            language='fr',
            format='1 vol. (186 p.) ; 23 cm',
            url=None,
        ) ,
        Book(
            title="Le dernier restaurant avant la fin du monde",
            author="Douglas Adams  ; traduit de l'anglais par Jean Bonnefoy",
            publisher='[Paris] : [Gallimard] , DL 2000',
            isbn13=9782070438617,
            publication_year=2000,
            abstract=(
                'La cuisine anglaise est exécrable. Moins abominable, cependant, que la poésie des Vogons, un peuple fier,'
                " ombrageux, et éminament irritable. D'ailleurs, les Vogons ont fait sauter la planète Terre, soi-disant p"
                "ar erreur. Pas de panique ! Grâce au fabuleux 'Guide du voyageur galactique', le pauvre Arthur Dent, ex-c"
                "itoyen britannique désormais apatride et passablement désemparé devant tant d'inconvenance, pourra affron"
                "ter sans crainte les improbables méandres d'un univers en folie. Rien ne l'empêchera, pas même un ascense"
                "ur dépressif, d'arriver à temps pour déguster le Plat du jour au Dernier Restaurant avant la Fin du Monde"
                '.'
            ),
            language='fr',
            format='1 vol. (279 p.) : couv. ill. en coul. ; 18 cm',
            url=None,
        ),
        Book(
            title='Moi, François le Français',
            author='Georges Piombo',
            publisher='Paris : Éditions Libre & Solidaire , 2022',
            isbn13=9782377940820,
            publication_year=2022,
            abstract=(
                "La vie est une aventure. Ma mère et mon père, une histoire d'amour au-dessus de tout. Il l'a enlevée, ils"
                " ont fait la « carrossela », sont partis sans se retourner, ont quitté le pays, la famiglia. Quand l'amou"
                "r est le plus fort, l'enfant paraît. L'enfant c'est moi, François le Français. Je veux être le meilleur F"
                "rançais possible, servir mon pays, m'émanciper ailleurs. D'autant plus qu'elle ne m'aime plus, ses soleil"
                "s ne brillent plus pour moi. Je m'en vais traverser la guerre, le siècle. Je veux devenir riche ; riche d"
                "e quoi ? La vie est une aventure, rencontrer l'autre est une jouissance."
            ),
            language='fr',
            format='1 vol. (186 p.) ; 23 cm',
            url=None,
        )
    ]
@app.get("/")
async def home(request: Request):

    context = {
        "request": request,
        "carousell_books" : booklist(),
    }
    return templates.TemplateResponse("index.html", context)

 
@app.get("/hello")  
def hello_func():  
  return "Hello World"  
 
@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)

# A private page that only logged in users can access.
@app.get("/private", response_class=HTMLResponse)
def index(request: Request, user: User = Depends(current_active_user)):
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("private.html", context)
 
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

import xml.etree.ElementTree as ET
from io import StringIO  
from rdflib import Graph, RDF
from app.books import Book, clean_isbn
from devtools import pprint, debug


# Example isbn
# 978-2013944762
# 9782253067900 
# 9782377940820
# 9782070438617
@app.get("/notice")  
async def hello_func(in_isbn: str):
        
    return isbn2book(in_isbn)

# Mount admin to your app
admin.mount_to(app)

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=80)
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)