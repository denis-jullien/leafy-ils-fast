from datetime import date
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from pydantic import PositiveInt, model_validator
from pydantic_extra_types.language_code import LanguageAlpha2

# from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from fastapi_users import schemas
from typing_extensions import Self
import uuid

# User (for authentification)


class User(SQLModelBaseUserDB, table=True):
    # first_name: str = Field(nullable=False)
    # last_name: str = Field(nullable=False)
    pass


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# Shared models


class SharedBase(SQLModel):
    archived: bool = Field(default=False, index=True)
    created_date: Optional[date] = None
    last_update_date: Optional[date] = None


class SharedUpdate(SQLModel):
    archived: Optional[bool] = None
    created_date: Optional[date] = None
    last_update_date: Optional[date] = None


class PaginationMetadata(SQLModel):
    total_items: int  # total number of items available in the dataset
    total_pages: int  # total number of pages


# Book


class BookBase(SharedBase):
    title: str = Field(index=True)
    author: str = Field(index=True)
    abstract: Optional[str] = None
    publisher: Optional[str] = None
    catalog: Optional[str] = Field(default=None, index=True)
    category_type: Optional[str] = Field(default=None, index=True)
    category_age: Optional[str] = Field(default=None, index=True)
    category_topics: Optional[str] = None
    language: Optional[LanguageAlpha2] = None
    cover: Optional[str] = None
    available: bool = Field(default=True, index=True)
    isbn: Optional[PositiveInt] = None
    format: Optional[str] = None
    publication_date: Optional[str] = None
    record_source: Optional[str] = None


class BookTable(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    circulation_history: list["CirculationTable"] = Relationship(back_populates="book")


class BookPublic(BookBase):
    id: int


class BooksPublic(SQLModel):
    data: list[BookPublic]
    meta: PaginationMetadata


class BookCreate(BookBase):
    pass


class BookUpdate(SharedUpdate):
    title: Optional[str] = None
    author: Optional[str] = None
    abstract: Optional[str] = None
    publisher: Optional[str] = None
    catalog: Optional[str] = None
    category_type: Optional[str] = None
    category_age: Optional[str] = None
    category_topics: Optional[str] = None
    language: Optional[LanguageAlpha2] = None
    cover: Optional[str] = None
    available: Optional[bool] = None
    isbn: Optional[PositiveInt] = None
    format: Optional[str] = None
    publication_date: Optional[str] = None


# Family


class FamilyBase(SharedBase):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    last_adhesion_date: Optional[date] = None

    @model_validator(mode="after")
    def check_rule_content(self) -> Self:
        if self.email is None and self.phone_number is None:
            raise ValueError(
                "A family must have at least one email or one phone number."
            )
        return self


class FamilyTable(FamilyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    members: list["MemberTable"] = Relationship(back_populates="family")


class FamilyPublic(FamilyBase):
    id: int


class FamiliesPublic(SQLModel):
    data: list[FamilyPublic]
    meta: PaginationMetadata


class FamilyCreate(FamilyBase):
    pass


class FamilyUpdate(SharedUpdate):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    last_adhesion_date: Optional[date] = None


# Member


class MemberBase(SharedBase):
    family_referent: bool = False
    firstname: str
    surname: str
    birthdate: Optional[date] = None
    family_id: Optional[int] = Field(default=None, foreign_key="familytable.id")


class MemberTable(MemberBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    family: Optional[FamilyTable] = Relationship(back_populates="members")
    circulation_history: list["CirculationTable"] = Relationship(
        back_populates="member"
    )


class MemberPublic(MemberBase):
    id: int


class MembersPublic(SQLModel):
    data: list[MemberPublic]
    meta: PaginationMetadata


class MemberCreate(MemberBase):
    pass


class MemberUpdate(SharedUpdate):
    family_referent: Optional[bool] = None
    firstname: Optional[str] = None
    surname: Optional[str] = None
    birthdate: Optional[date] = None
    family_id: Optional[int] = None


# Circulation


class CirculationBase(SharedBase):
    borrowed_date: date
    returned_date: Optional[date] = None

    book_id: int = Field(default=None, foreign_key="booktable.id")
    member_id: int = Field(default=None, foreign_key="membertable.id")


class CirculationTable(CirculationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book: BookTable = Relationship(back_populates="circulation_history")
    member: MemberTable = Relationship(back_populates="circulation_history")


class CirculationPublic(CirculationBase):
    id: int


class CirculationsPublic(SQLModel):
    data: list[CirculationPublic]
    meta: PaginationMetadata


class CirculationCreate(CirculationBase):
    pass


class CirculationUpdate(SharedUpdate):
    borrowed_date: Optional[date] = None
    returned_date: Optional[date] = None
    book_id: Optional[int] = None
    member_id: Optional[int] = None


# Public relationship


class MemberPublicWithFamily(MemberPublic):
    family: Optional[FamilyPublic] = None


class FamilyPublicWithMembers(FamilyPublic):
    members: list[MemberPublic] = []


class CirculationPublicWithRelationship(CirculationPublic):
    book: Optional[BookPublic] = None
    member: Optional[MemberPublic] = None
