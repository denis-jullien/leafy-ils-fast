import logging
import os

from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from ..database import create_db_and_tables, global_engine, get_session
from ..models import (
    MemberTable,
    MemberPublic,
    MemberCreate,
    MemberUpdate,
    MemberSearch,
    MemberPublicWithFamily,
)

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


@router.get("", response_model=list[MemberPublic])
def read_members(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    members = session.exec(select(MemberTable).offset(offset).limit(limit)).all()
    return members


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


@router.delete("/{member_id}")
def delete_member(*, session: Session = Depends(get_session), member_id: int):
    member = session.get(MemberTable, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    session.delete(member)
    session.commit()
    return {"ok": True}
