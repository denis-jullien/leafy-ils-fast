
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..database import get_session
from ..models import BookTable, BookPublic, BookCreate, BookUpdate

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


@router.get("", response_model=list[BookPublic])
def read_books(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
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
