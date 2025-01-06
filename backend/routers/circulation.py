from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from backend.database import get_session
from backend.models import (
    CirculationTable,
    CirculationPublic,
    CirculationsPublic,
    CirculationCreate,
    CirculationUpdate,
    CirculationPublicWithRelationship,
    PaginationMetadata,
)
from ..internals import constants


import math

router = APIRouter(
    prefix="/circulations",
    tags=["circulations"],
)


@router.post("", response_model=CirculationPublic)
def create_circulation(
    *, session: Session = Depends(get_session), circulation: CirculationCreate
):
    db_data = CirculationTable.model_validate(circulation)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return db_data


@router.get("", response_model=CirculationsPublic)
def read_circulations(
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
    circulations = session.exec(
        select(CirculationTable).offset(offset).limit(limit)
    ).all()

    # Query total item count
    total_items = len(session.exec(select(CirculationTable)).all())
    # Calculate total pages
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    metadata = PaginationMetadata(
        total_items=total_items,
        total_pages=total_pages,
    )

    return CirculationsPublic(data=circulations, meta=metadata)


@router.get("/{circulation_id}", response_model=CirculationPublicWithRelationship)
def read_circulation(*, session: Session = Depends(get_session), circulation_id: int):
    circulation = session.get(CirculationTable, circulation_id)
    if not circulation:
        raise HTTPException(status_code=404, detail="Circulation not found")
    return circulation


@router.patch("/{circulation_id}", response_model=CirculationPublic)
def update_circulation(
    *,
    session: Session = Depends(get_session),
    circulation_id: int,
    circulation: CirculationUpdate,
):
    db_circulation = session.get(CirculationTable, circulation_id)
    if not db_circulation:
        raise HTTPException(status_code=404, detail="Circulation not found")
    circulation_data = circulation.model_dump(exclude_unset=True)
    db_circulation.sqlmodel_update(circulation_data)
    session.add(db_circulation)
    session.commit()
    session.refresh(db_circulation)
    return db_circulation


@router.delete("/{circulation_id}", status_code=204)
def delete_circulation(*, session: Session = Depends(get_session), circulation_id: int):
    circulation = session.get(CirculationTable, circulation_id)
    if not circulation:
        raise HTTPException(status_code=404, detail="Circulation not found")
    session.delete(circulation)
    session.commit()
    return
