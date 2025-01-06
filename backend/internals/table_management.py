from backend.models import (
    PaginationMetadata,
)
from ..internals import constants
from sqlalchemy.sql import func
from sqlmodel import Session

import math


def get_paginate_metadata(
    session: Session, statement: constants.STATEMENT_TYPE, limit: int
) -> PaginationMetadata:
    """Get metadata from a table from a statement

    Parameters
    ----------
    statement:
        result of SQLModel select
        ex: statement = select(Book)
    limit

    Returns
    ----------
    PaginationMetadata
    """
    # Query total item count
    total_items = len(session.exec(statement).all())
    # Calculate total pages
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    metadata = PaginationMetadata(
        total_items=total_items,
        total_pages=total_pages,
    )
    return metadata


def normalize_string(string: str) -> str:
    """normalize strings (case-insensitive, remove spaces and special characters)"""
    return func.replace(func.replace(func.lower(string), " ", ""), "-", "")
