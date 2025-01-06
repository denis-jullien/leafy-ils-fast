from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from backend.database import get_session
from backend.models import (
    MemberTable,
    MemberPublic,
    MembersPublic,
    MemberCreate,
    MemberUpdate,
    MemberPublicWithFamily,
    PaginationMetadata,
)
from ..internals import constants

import math

router = APIRouter(
    prefix="/members",
    tags=["members"],
)


@router.post("", response_model=MemberPublic)
def create_member(*, session: Session = Depends(get_session), member: MemberCreate):
    db_data = MemberTable.model_validate(member)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)
    return db_data


@router.get("", response_model=MembersPublic)
def read_members(
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
    members = session.exec(select(MemberTable).offset(offset).limit(limit)).all()
    # Query total item count
    total_items = len(session.exec(select(MemberTable)).all())
    # Calculate total pages
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

    metadata = PaginationMetadata(
        total_items=total_items,
        total_pages=total_pages,
    )

    return MembersPublic(data=members, meta=metadata)


@router.get("/{member_id}", response_model=MemberPublicWithFamily)
def read_member(*, session: Session = Depends(get_session), member_id: int):
    member = session.get(MemberTable, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.patch("/{member_id}", response_model=MemberPublic)
def update_member(
    *, session: Session = Depends(get_session), member_id: int, member: MemberUpdate
):
    db_member = session.get(MemberTable, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    member_data = member.model_dump(exclude_unset=True)
    db_member.sqlmodel_update(member_data)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@router.delete("/{member_id}", status_code=204)
def delete_member(*, session: Session = Depends(get_session), member_id: int):
    member = session.get(MemberTable, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    session.delete(member)
    session.commit()
    return
