from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing_extensions import Annotated
from backend.config import get_settings, Settings
from backend.database import get_session
from backend.models import BookTable, BookPublic, BooksPublic, BookCreate, BookUpdate
from backend.internals.book_notice import isbn2book
from ..internals import constants
from ..internals.table_management import get_paginate_metadata


router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("", response_model=BookPublic)
def create_book(*, session: Session = Depends(get_session), book: BookCreate):
    db_data = BookTable.model_validate(book)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return db_data


@router.post("/{isbn}", response_model=BookPublic)
async def create_book_isbn(
    *,
    session: Session = Depends(get_session),
    settings: Annotated[Settings, Depends(get_settings)],
    isbn: str,
):
    """
    Isbn for reference :\n
    978-2013944762
    9782253067900
    9782377940820
    9782070438617
    9780738531366
    9782253072980
    9781632658128
    9782361934996
    9782815310253
    """
    book = await isbn2book(isbn, settings)

    if book is None:
        raise HTTPException(status_code=400, detail="Item not found")

    db_data = BookTable.model_validate(book)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return db_data


@router.get("", response_model=BooksPublic)
def read_books(
    *,
    session: Session = Depends(get_session),
    page: int = Query(
        default=constants.DEFAULT_MINIMAL_VALUE, ge=constants.DEFAULT_MINIMAL_VALUE
    ),
    limit: int = Query(
        default=constants.LIMIT_DEFAULT_VALUE,
        le=constants.LIMIT_MAXIMAL_VALUE,
        ge=constants.DEFAULT_MINIMAL_VALUE,
    ),
    filter_available: bool = Query(default=None, alias="filter[available]"),
    filter_archived: bool = Query(default=None, alias="filter[archived]"),
):
    offset = (page - 1) * limit

    # Filter data
    statement = select(BookTable)
    if filter_archived is not None:
        statement = statement.where(BookTable.archived == filter_archived)
    if filter_available is not None:
        statement = statement.where(BookTable.available == filter_available)

    # Return paginated data
    books = session.exec(statement.offset(offset).limit(limit)).all()
    metadata = get_paginate_metadata(session, select(BookTable), limit)

    return BooksPublic(data=books, meta=metadata)


@router.get("/{book_id}", response_model=BookPublic)
def read_book(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(BookTable, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=BookPublic)
def update_book(
    *, session: Session = Depends(get_session), book_id: int, book: BookUpdate
):
    db_book = session.get(BookTable, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_data)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=204)
def delete_book(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(BookTable, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return
