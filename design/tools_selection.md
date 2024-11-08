# Technical idea

Following our constraints, we will look in priority for opensource tools.

TODO: add more information here

```mermaid
flowchart TD
    subgraph Backend
    Auth
    end
    Frontend <--> Backend
    Backend <--> Database[(Database)]
```

TODO: add more information here

## Other Ideas

Django
ReactJS
SvelteKit

## Solution

- Frontend
    - [HTMx](https://htmx.org/)
    - [daisyui](https://htmx.org/)
- Backend
    - [FastAPI](https://fastapi.tiangolo.com/)
    - Auth
        - [FastAPI Users](https://fastapi-users.github.io/fastapi-users/10.1/)
- ORM
    - [SQLModel](https://sqlmodel.tiangolo.com/)
- DataBase
    - [SQLite](https://www.sqlite.org/)

```mermaid
flowchart TD
    subgraph Backend["FastAPI (Backend)"]
    Auth["FastAPI Users (Auth)"]
    end
    Frontend["HTMx (Frontend)"] <--API REST--> Backend
    Backend <--SQLModel--> Database[(SQLite)]
```
