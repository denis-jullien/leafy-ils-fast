from datetime import date
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


# Shared models


class SharedBase(SQLModel):
    archived: bool = Field(default=False, index=True)
    registration_date: Optional[date] = None
    # last_update_date: Optional[date] = None


class SharedUpdate(SQLModel):
    archived: Optional[bool] = None
    registration_date: Optional[date] = None
    # last_update_date: Optional[date] = None


# Book


class BookBase(SharedBase):
    title: str = Field(index=True)
    author: str = Field(index=True)
    synopsis: Optional[str] = None
    edition: Optional[str] = None
    catalog: Optional[str] = Field(default=None, index=True)
    category_type: Optional[str] = Field(default=None, index=True)
    category_age: Optional[str] = Field(default=None, index=True)
    category_topics: Optional[str] = None
    langage: Optional[str] = None
    cover: Optional[str] = None
    available: bool = Field(default=True, index=True)
    # history: list["BorrowHistory"] = Relationship(back_populates="book")


class BookTable(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class BookPublic(BookBase):
    id: int


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


class BookSearch(BookUpdate):
    pass
