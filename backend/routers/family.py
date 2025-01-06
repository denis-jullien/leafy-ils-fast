from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from backend.database import get_session
from backend.models import (
    FamilyTable,
    FamilyPublic,
    FamilyCreate,
    FamilyUpdate,
    FamilyPublicWithMembers,
    FamiliesPublic,
    PaginationMetadata,
)
from ..internals import constants

import math

router = APIRouter(
    prefix="/families",
    tags=["families"],
)


@router.post("", response_model=FamilyPublic)
def create_family(*, session: Session = Depends(get_session), family: FamilyCreate):
    db_data = FamilyTable.model_validate(family)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return db_data


@router.get("", response_model=FamiliesPublic)
def read_families(
    *,
    session: Session = Depends(get_session),
    page: int = Query(
        default=constants.DEFAULT_MINIMAL_VALUE, ge=constants.DEFAULT_MINIMAL_VALUE
    ),
    limit: int = Query(
        default=constants.LIMIT_DEFAULT_VALUE,
        le=constants.LIMIT_MAXIMAL_VALUE,
        ge=constants.DEFAULT_MINIMAL_VALUE,
    ),
):
    offset = page * limit - limit
    families = session.exec(select(FamilyTable).offset(offset).limit(limit)).all()

    # Query total item count
    total_items = len(session.exec(select(FamilyTable)).all())
    # Calculate total pages
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    metadata = PaginationMetadata(
        total_items=total_items,
        total_pages=total_pages,
    )

    return FamiliesPublic(data=families, meta=metadata)


@router.get("/{family_id}", response_model=FamilyPublicWithMembers)
def read_family(*, session: Session = Depends(get_session), family_id: int):
    family = session.get(FamilyTable, family_id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family


@router.patch("/{family_id}", response_model=FamilyPublic)
def update_family(
    *, session: Session = Depends(get_session), family_id: int, family: FamilyUpdate
):
    db_family = session.get(FamilyTable, family_id)
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    family_data = family.model_dump(exclude_unset=True)
    db_family.sqlmodel_update(family_data)
    session.add(db_family)
    session.commit()
    session.refresh(db_family)
    return db_family


@router.delete("/{family_id}", status_code=204)
def delete_family(*, session: Session = Depends(get_session), family_id: int):
    family = session.get(FamilyTable, family_id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    session.delete(family)
    session.commit()
    return
