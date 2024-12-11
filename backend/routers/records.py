from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated
from backend.config import get_settings, Settings


from backend.models import BookCreate
from backend.internals.book_record import isbn2book


router = APIRouter(
    prefix="/records",
    tags=["Records"],
)


@router.post("/{isbn}", response_model=BookCreate)
async def find_book_by_isbn(
    *,
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

    return book