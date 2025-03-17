import datetime
import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Students, Groups
from app.api.schemas import StudentSchema, GroupsSchema


def create_group(db: Session, group: Groups):
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_groups(db: Session):
    return db.query(Groups).all()


def get_group_by_id(db: Session, group_id: uuid.UUID):
    return db.query(Groups).filter(Groups.id == group_id).first()


def delete_group(db: Session, group_id: uuid.UUID):
    deleted = db.query(Groups).filter(Groups.id == group_id).delete()
    db.commit()
    return deleted


def update_group(db: Session, group: GroupsSchema, group_id: uuid.UUID):

    _group = get_group_by_id(db=db, group_id=group_id)
    _group.updated_at = datetime.datetime.now()
    update_data = group.model_dump(exclude_unset=True)

    for field_name, field_value in update_data.items():
        setattr(_group, field_name, field_value)

    db.commit()
    db.refresh(_group)
    return _group


def count_groups(db: Session):
    return db.query(func.count(Groups.id)).scalar()
