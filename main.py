from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import logging

from app.books import Book
from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, auth_cookie_backend, current_active_user, fastapi_users
from app.admin import admin
from app.routers import book

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(book.router)

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
            url=""
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
            url="",
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
            url="",
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
            url="",
        )
    ]



@app.get("/")
async def home(request: Request):

    context = {
        "request": request,
        "carousell_books" : booklist(),
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/books")
async def books(request: Request):


    return booklist()+ booklist()+ booklist()

 
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# Mount admin to your app
admin.mount_to(app)

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=80)
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)