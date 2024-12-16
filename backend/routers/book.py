from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing_extensions import Annotated
from backend.config import get_settings, Settings

from backend.database import get_session
from backend.models import BookTable, BookPublic, BookCreate, BookUpdate
from backend.internals.book_notice import isbn2book
from ..internals import constants


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


@router.get("", response_model=list[BookPublic])
def read_books(
    *,
    session: Session = Depends(get_session),
    page: int = Query(
        default=constants.PAGE_DEFAULT_VALUE, ge=constants.PAGE_MINIMAL_VALUE
    ),
    limit: int = Query(
        default=constants.LIMIT_DEFAULT_VALUE,
        le=constants.LIMIT_MAXIMAL_VALUE,
        ge=constants.LIMIT_MINIMAL_VALUE,
    ),
):
    offset = page * limit - limit
    books = session.exec(select(BookTable).offset(offset).limit(limit)).all()
    return books


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


@router.delete("/{book_id}")
def delete_book(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(BookTable, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}
