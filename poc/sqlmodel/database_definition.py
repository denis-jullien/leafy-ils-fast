import datetime

from enum import Enum
from pydantic import BaseModel, field_validator, ValidationError, ValidationInfo
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


DEFAULT_LANGAGE = "français"


class CategoryType(str, Enum):
    NOVEL = "roman"
    SHORT_STORIES = "nouvelles"
    COMIC = "bande-dessinée"
    DOC = "documentaire"
    ALBUM = "album"
    BABY = "cartonné"


class CategoryAge(int, Enum):
    SENIOR = 60
    ADULTE = 18
    ADO = 12
    KID = 6
    TODDLER = 3
    BABY = 0


class CategoryTopic(str, Enum):
    DETECTIVE = "policier"
    MANGA = "manga"


class Catalog(str, Enum):
    US = "arbousiers"
    COUNTY_LIBRARY = "Pierre-Vives"


# class Book(SQLModel, table=True):

#     class Category(SQLModel):
#         type: CategoryType
#         age: CategoryAge
#         topic: Optional[list[CategoryTopic]] = None

#     class BorrowDetails(SQLModel):
#         available: bool = True
#         history: list["BorrowHistory"] = Relationship(back_populates="book")

#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str = Field(index=True)
#     author: str = Field(index=True)
#     synopsis: str
#     edition: str
#     category: Category = Field(index=True)
#     catalog: Catalog = Field(index=True)
#     langage: Optional[str] = DEFAULT_LANGAGE
#     cover: Optional[str] = None
#     registration_date: datetime.date

#     borrow_details: BorrowDetails

# class BorrowHistory(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)

#     release_date: datetime.date
#     return_date: Optional[datetime.date] = None

#     # book_id: int = Field(default=None, foreign_key="book.id")
#     book: Book = Relationship(back_populates="history")
#     # member_id: int = Field(default=None, foreign_key="familyMember.id")
#     member: "FamilyMember" = Relationship(back_populates="borrow_history")


class Family(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    members: list["FamilyMember"] = Relationship(back_populates="family")
    email: Optional[str]
    phone_number: Optional[str]
    last_adhesion_date: datetime.date

    @field_validator("phone_number", "email")
    @classmethod
    def check_contact(cls, v: dict, info: ValidationInfo):
        phone_number = info.data["phone_number"]
        email = info.data["email"]

        if phone_number is None and email is None:
            raise ValueError(
                f"At least on contact details must be set among phone_number '{phone_number}' and email '{email}'."
            )


class FamilyMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    family_referent: bool = False
    firstname: str
    surname: str
    birthdate: Optional[datetime.date]
    family_id: Optional[int] = Field(default=None, foreign_key="family.id")
    family: Optional[Family] = Relationship(back_populates="members")
    # borrow_history: list["BorrowHistory"] = Relationship(back_populates="book")
