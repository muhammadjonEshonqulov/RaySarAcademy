import datetime
import uuid
from typing import Optional
from fastapi import HTTPException
from pydantic.v1 import UUID1

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Students, UsersTemp
from app.api.schemas import StudentSchema, UserTempSchema


def get_student(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        order_by: Optional[str] = None,
        search: Optional[str] = None,
):
    if skip < 0:
        skip = 0
    query = db.query(Students)
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Students.name.ilike(search), Students.surname.ilike(search)))

    if order_by == "descend":
        query = query.order_by(Students.name.desc())
    elif order_by == "ascend":
        query = query.order_by(Students.name.asc())
    else:
        query = query.order_by(Students.created_at.desc())

    return query.offset(skip * limit).limit(limit).all(), query.count()


def count_students(db: Session):
    return db.query(func.count(Students.id)).scalar()


def get_students(db: Session):
    return db.query(Students).all()


def get_student_by_id(db: Session, student_id: uuid.UUID):
    return db.query(Students).filter(Students.id == student_id).first()


def delete_student(db: Session, student_id: uuid.UUID):
    db.query(Students).filter(Students.id == student_id).delete()
    db.commit()


def update_student(db: Session, student: StudentSchema, student_id: uuid.UUID):
    _student = get_student_by_id(db=db, student_id=student_id)
    if not _student:
        raise HTTPException(status_code=422, detail="Student not found")
    update_data = student.model_dump(exclude_unset=True)

    for field_name, field_value in update_data.items():
        setattr(_student, field_name, field_value)

    db.commit()
    db.refresh(_student)
    return _student


def get_user_temp_by_id(db: Session, user_temp_id: uuid.UUID):
    return db.query(UsersTemp).filter(UsersTemp.id == user_temp_id).first()


def get_user_temps(db: Session):
    return db.query(UsersTemp).filter(UsersTemp.role == None).all()


def delete_user_temp(db: Session, user_temp_id: uuid.UUID):
    db.query(UsersTemp).filter(UsersTemp.id == user_temp_id).delete()
    db.commit()


def update_user_temp_role(db: Session, user_temp_id: uuid.UUID, role: str):
    _user_temp = get_user_temp_by_id(db=db, user_temp_id=user_temp_id)
    if not _user_temp:
        raise HTTPException(status_code=422, detail="User not found")

    _user_temp.role = role
    _user_temp.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(_user_temp)
    return _user_temp
