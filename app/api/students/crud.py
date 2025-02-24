import datetime
import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session


from app.api.models import Students
from app.api.schemas import StudentSchema


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
        query = query.filter(or_(Students.first_name.ilike(search), Students.second_name.ilike(search)))

    if order_by == "descend":
        query = query.order_by(Students.first_name.desc())
    elif order_by == "ascend":
        query = query.order_by(Students.first_name.asc())
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

def create_student(db: Session, student: Students):
    _student = get_student_by_id(db=db, student_id=student.id)
    if _student:
        raise HTTPException(status_code=422, detail="Student already exists")
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: StudentSchema, student_id: uuid.UUID):
    _student = get_student_by_id(db=db, student_id=student_id)

    update_data = student.model_dump(exclude_unset=True)

    for field_name, field_value in update_data.items():
        setattr(_student, field_name, field_value)

    db.commit()
    db.refresh(_student)
    return _student
