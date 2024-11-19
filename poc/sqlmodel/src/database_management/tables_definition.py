from datetime import date

from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

EMPTY_STRING = ""


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    synopsis: Optional[str] = EMPTY_STRING
    edition: Optional[str] = EMPTY_STRING
    catalog: Optional[str] = Field(default=EMPTY_STRING, index=True)
    category_type: Optional[str] = Field(default=EMPTY_STRING, index=True)
    category_age: Optional[str] = Field(default=EMPTY_STRING, index=True)
    category_topics: Optional[str] = EMPTY_STRING
    langage: Optional[str] = EMPTY_STRING
    cover: Optional[str | None] = None

    available: bool = Field(default=True, index=True)
    archived: bool = Field(default=False, index=True)
    history: list["BorrowHistory"] = Relationship(back_populates="book")

    registration_date: date
    last_update_date: date


class BorrowHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    release_date: date
    return_date: Optional[date | None] = None

    book_id: int = Field(default=None, foreign_key="book.id")
    book: Book = Relationship(back_populates="history")
    # member_id: int = Field(default=None, foreign_key="familyMember.id")
    # member: "FamilyMember" = Relationship(back_populates="borrow_history")


class Family(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    members: list["FamilyMember"] = Relationship(back_populates="family")
    email: Optional[str]
    phone_number: Optional[str]
    last_adhesion_date: date
    archived: bool = Field(default=False, index=True)


class FamilyMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    family_referent: bool = False
    firstname: str
    surname: str
    birthdate: Optional[date] = None
    family_id: Optional[int] = Field(default=None, foreign_key="family.id")
    family: Optional[Family] = Relationship(back_populates="members")
    archived: bool = Field(default=False, index=True)
    # borrow_history: list["BorrowHistory"] = Relationship(back_populates="book")
