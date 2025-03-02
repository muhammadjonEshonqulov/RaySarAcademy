import datetime
import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Admins
from app.api.schemas import AdminsSchema


def get_admin(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        search: Optional[str] = None,
):
    if skip < 0:
        skip = 0
    query = db.query(Admins)
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Admins.name.ilike(search), Admins.surname.ilike(search)))

    if order_by == "descend":
        query = query.order_by(Admins.name.desc())
    elif order_by == "ascend":
        query = query.order_by(Admins.name.asc())
    else:
        query = query.order_by(Admins.created_at.desc())

    return query.offset(skip * limit).limit(limit).all(), query.count()


def count_admins(db: Session):
    return db.query(func.count(Admins.id)).scalar()


def get_admins(db: Session):
    return db.query(Admins).filter(Admins.role == 'admin').all()

def get_teachers(db: Session):
    return db.query(Admins).filter(Admins.role == 'teacher').all()


def get_admin_by_id(db: Session, admin_id: uuid.UUID):
    return db.query(Admins).filter(Admins.id == admin_id).first()


def create_admin(db: Session, admin: Admins):
    _admin = get_admin_by_id(db=db, admin_id=admin.id)
    if _admin.role == 'teacher':
        raise HTTPException(status_code=422, detail="Teacher already exists")
    if _admin.role == 'admin':
        raise HTTPException(status_code=422, detail="Admin already exists")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin_id: uuid.UUID):
    db.query(Admins).filter(Admins.id == admin_id).delete()
    db.commit()



def update_admin(db: Session, admin: AdminsSchema, admin_id: uuid.UUID):
    _admin = get_admin_by_id(db=db, admin_id=admin_id)

    update_data = admin.model_dump(exclude_unset=True)

    for field_name, field_value in update_data.items():
        setattr(_admin, field_name, field_value)

    db.commit()
    db.refresh(_admin)
    return _admin
