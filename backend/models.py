from datetime import date
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


# Shared models


class SharedBase(SQLModel):
    archived: bool = Field(default=False, index=True)
    created_date: Optional[date] = None
    last_update_date: Optional[date] = None


class SharedUpdate(SQLModel):
    archived: Optional[bool] = None
    created_date: Optional[date] = None
    last_update_date: Optional[date] = None


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


class BookTable(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    circulation_history: list["CirculationTable"] = Relationship(back_populates="book")


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


# Family


class FamilyBase(SharedBase):
    email: Optional[str]
    phone_number: Optional[str]
    # last_adhesion_date: Optional[date] = None


class FamilyTable(FamilyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    members: list["MemberTable"] = Relationship(back_populates="family")


class FamilyPublic(FamilyBase):
    id: int


class FamilyCreate(FamilyBase):
    pass


class FamilyUpdate(SharedUpdate):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    # last_adhesion_date: Optional[date] = None


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
