import uuid

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.api.models import Students, Admins
from app.api.schemas import Response, AdminsSchema, StudentSchema
from app.api.admins.crud import (
    get_admin,
    get_admin_by_id,
    create_admin,
    delete_admin,
    update_admin,
)
from app.api.sessians.crud import update_user_temp_role, get_user_temps
from app.api.students.crud import create_student
from app.db import get_db
from app.utils.auth_middleware import get_current_admin

router = APIRouter()


@router.get("/admin-me")
async def get_admin_by_id_route(
        db: Session = Depends(get_db),
        current_admin: dict = Depends(get_current_admin),
):
    _admin = get_admin_by_id(db, current_admin["id"])
    return Response(
        code=200, success=True, message="success", data=_admin
    ).model_dump()


@router.get("/get_admin/{admin_id}")
async def get_admin_by_id_route(
        admin_id: uuid.UUID,
        db: Session = Depends(get_db),
        _=Depends(get_current_admin),
):
    _admin = get_admin_by_id(db, admin_id)
    return Response(code=200, success=True, message="success", data=_admin).model_dump()


@router.get("/set_role")
async def set_role(
        use_temp_id: uuid.UUID,
        role: str,
        db: Session = Depends(get_db),
        _=Depends(get_current_admin),
):
    _user_temp = update_user_temp_role(db, use_temp_id, role)
    if not _user_temp:
        raise HTTPException(status_code=422, detail="User not found")

    update_user_temp_role(db, use_temp_id, role)
    if role == "student":
        _student = Students(id=use_temp_id, name=_user_temp.name, surname=_user_temp.surname,
                            updated_at=_user_temp.updated_at, role=role,
                            created_at=_user_temp.created_at, password=_user_temp.password,
                            address=_user_temp.address, phone_number=_user_temp.phone_number,
                            date_birth=_user_temp.date_birth, gender=_user_temp.gender)

        _user_temp = create_student(db, _student)
    else:
        _admin = Admins(id=use_temp_id, name=_user_temp.name, surname=_user_temp.surname,
                        updated_at=_user_temp.updated_at, role=role,
                        created_at=_user_temp.created_at, address=_user_temp.address,
                        phone_number=_user_temp.phone_number, password=_user_temp.password,
                        date_birth=_user_temp.date_birth, gender=_user_temp.gender)

        _user_temp = create_admin(db, _admin)

    return Response(code=201, success=True, message="successs", data=_user_temp).model_dump()


@router.get("/get_Admins")
async def get_Admins_route(
        req: Request,
        db: Session = Depends(get_db),
        _=Depends(get_current_admin),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    debt = req.query_params.get("debt")
    _Admins, _count_of_Admins = get_admin(
        db,
        limit=limit,
        skip=skip,
        order_by=req.query_params.get("order"),
        search=req.query_params.get("search"),
    )
    return Response(
        code=200,
        success=True,
        message="success",
        data=[
            {
                "id": admin.id,
                "name": admin.name,
                "surname": admin.surname,
                "date_birth": admin.date_birth,
                "address": admin.address,
                "phone_number": admin.phone_number,
                "gender": admin.gender,
                "created_at": admin.created_at,
                "updated_at": admin.updated_at,
            }
            for admin in _Admins
        ],
    ).model_dump()


@router.get("/get_registered")
async def get_registered_route(
        db: Session = Depends(get_db),
        _=Depends(get_current_admin),
):
    data = get_user_temps(db)
    return Response(code=200, success=True, message="ok", data=data).model_dump()


@router.delete("/delete_admin/{admin_id}")
async def delete_admin_route(
        admin_id: uuid.UUID,
        db: Session = Depends(get_db),
        _=Depends(get_current_admin),
):
    delete_admin(db, admin_id)
    return Response(
        code=200,
        success=True,
        message="deleted",
    ).model_dump()


@router.put("/update_admin/{admin_id}")
async def update_admin_route(
        admin_id: uuid.UUID,
        admin: AdminsSchema,
        db: Session = Depends(get_db),
        _=Depends(get_current_admin),
):
    _admin = update_admin(db, admin, admin_id)
    return Response(code=200, success=True, message="updated", data=_admin).model_dump()
