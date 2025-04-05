from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth.crud import get_admin_from_by_login, get_student_from_by_login
from app.api.models import Students, Admins, UsersTemp
from app.api.schemas import LoginSchema, Response, StudentSchema
from app.db import get_db
from app.utils.auth_middleware import create_access_token
from app.utils.constants import ACCESS_TOKEN_EXPIRE_WEEKS

router = APIRouter()


@router.post("/login")
async def login(staff: LoginSchema, db: Session = Depends(get_db)):
    _current_admin = get_admin_from_by_login(db=db, login=staff.login)
    print('_current_admin=>', _current_admin)
    if _current_admin:
        return await admin_login(staff, _current_admin)

    _current_student = get_student_from_by_login(db=db, login=staff.login)
    print('_current_student=>', _current_student)

    if _current_student:
        return await student_login(staff, _current_student)

    raise HTTPException(status_code=401, detail="Siz ro'yxatdan o'tmagansiz")


async def admin_login(admin: LoginSchema, _current_admin: Admins):
    check_password = _current_admin.password == admin.password
    if not check_password:
        raise HTTPException(status_code=401, detail="Parol notog'ri")
    return Response(
        code=200,
        success=True,
        message="Successfully login",
        data={
            "role": _current_admin.role,
            "access_token": create_access_token(
                data={"id": str(_current_admin.id), "role": _current_admin.role},
                expires_delta=timedelta(weeks=int(ACCESS_TOKEN_EXPIRE_WEEKS)),
            ),
        },
    ).model_dump()


async def student_login(student: LoginSchema, _current_student: Students):
    check_password = _current_student.password == student.password
    if not check_password:
        raise HTTPException(status_code=401, detail="Parol notog'ri")
    return Response(
        code=200,
        success=True,
        message="Successfully login",
        data={
            "role": _current_student.role,
            "access_token": create_access_token(
                data={"id": str(_current_student.id), "role": _current_student.role},
                expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_WEEKS)),
            ),
        },
    ).model_dump()


@router.post("/register")
async def register(student: StudentSchema, db: Session = Depends(get_db)):
    existing_user_temp = db.query(UsersTemp).filter(UsersTemp.phone_number == student.phone_number).first() or db.query(
        Students).filter(Students.phone_number == student.phone_number).first() or db.query(Admins).filter(
        Admins.phone_number == student.phone_number).first()

    if existing_user_temp:
        raise HTTPException(status_code=422, detail="Bu telefon raqam allaqachon mavjud")

    new_user_temp = UsersTemp(
        id=student.id,
        phone_number=student.phone_number,
        name=student.name,
        surname=student.surname,
        password=student.password,
        role=student.role,
        created_at=student.created_at,
        updated_at=student.updated_at,
    )

    db.add(new_user_temp)
    db.commit()
    db.refresh(new_user_temp)

    return {
        "code": 201,
        "success": True,
        "message": "Successfully registered",
        "data": new_user_temp,
    }
