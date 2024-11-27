from datetime import date
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


EMPTY_STRING = ""

# Shared models


class SharedBase(SQLModel):
    archived: bool = Field(default=False, index=True)
    # last_update_date: Optional[date] = None


class SharedUpdate(SQLModel):
    archived: Optional[bool] = None
    # last_update_date: Optional[date] = None


class AuthorBookTableLink(SQLModel, table=True):
    author_id: Optional[int] = Field(
        default=None, foreign_key="authortable.id", primary_key=True
    )
    book_id: Optional[int] = Field(
        default=None, foreign_key="booktable.id", primary_key=True
    )
    author_role: Optional[str] = None
    author: "AuthorTable" = Relationship(back_populates="book_links")
    book: "BookTable" = Relationship(back_populates="author_links")


# Author


class AuthorBase(SharedBase):
    name: str = Field(index=True)
    description: Optional[str] = EMPTY_STRING


class AuthorTable(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: list["AuthorBookTableLink"] = Relationship(back_populates="author")


class AuthorPublic(AuthorBase):
    id: int
    books: list["BookPublic"] = []


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(SQLModel):
    name: str | None = None
    description: str | None = None


class AuthorSearch(AuthorUpdate):
    pass


# Book


class BookBase(SharedBase):
    title: str = Field(index=True)
    author: str = Field(index=True)
    synopsis: Optional[str] = EMPTY_STRING
    edition: Optional[str] = EMPTY_STRING
    catalog: Optional[str] = Field(default=EMPTY_STRING, index=True)
    category_type: Optional[str] = Field(default=EMPTY_STRING, index=True)
    category_age: Optional[str] = Field(default=EMPTY_STRING, index=True)
    category_topics: Optional[str] = EMPTY_STRING
    langage: Optional[str] = EMPTY_STRING
    cover: Optional[str] = None

    available: bool = Field(default=True, index=True)
    # history: list["BorrowHistory"] = Relationship(back_populates="book")

    registration_date: Optional[date] = None


class BookTable(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    authors: list[AuthorBookTableLink] = Relationship(back_populates="book")


class BookPublic(BookBase):
    id: int
    authors: list["AuthorPublic"] = []


class BookCreate(BookBase):
    pass


class BookUpdate(SharedUpdate):
    title: Optional[str] = None
    author: Optional[str] = None
    synopsis: Optional[str] = None
    edition: Optional[str] = None
    catalog: Optional[str] = None
    category_type: Optional[str] = None
    category_age: Optional[str] = None
    category_topics: Optional[str] = None
    langage: Optional[str] = None
    cover: Optional[str] = None
    available: Optional[bool] = None
    registration_date: Optional[date] = None


class BookSearch(BookUpdate):
    pass
