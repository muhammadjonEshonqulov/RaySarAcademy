# import uuid
# from fastapi import APIRouter, Depends, Request
import uuid

# students/router.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from typing import List
import os, shutil

from requests import Session

from app.api.groups.crud import create_group, get_groups, get_group_by_id, delete_group, update_group
from app.api.models import Groups
from app.api.schemas import Response, GroupsSchema
from app.db import get_db
from app.utils.auth_middleware import get_current_admin

router = APIRouter()


@router.post("/add_group")
async def add_group(
        group: GroupsSchema,
        db: Session = Depends(get_db),
        _admin=Depends(get_current_admin),
):
    if _admin['role'] == 'admin' or _admin['role'] == 'teacher':
        db_group = Groups(
            name=group.name,
            science_name=group.science_name,
            created_at=group.created_at,
            updated_at=group.updated_at
        )
        _group = create_group(db, db_group)
        return Response(code=201, success=True, message="success", data=_group).model_dump()
    else:
        raise HTTPException(status_code=422, detail="Ushbu userda bunday amalni bajarishga huquqi yo'q")


@router.get("/get_groups")
async def get_group(
        db: Session = Depends(get_db),
        _admin=Depends(get_current_admin),
):
    if _admin['role'] == 'admin' or _admin['role'] == 'teacher':
        db_groups = get_groups(db)
        return Response(code=200, success=True, message="success", data=db_groups).model_dump()
    else:
        raise HTTPException(status_code=422, detail="Ushbu userda bunday amalni bajarishga huquqi yo'q")

@router.get("/get_group/{group_id}")
async def get_group(
        group_id: uuid.UUID,
        db: Session = Depends(get_db),
        _admin=Depends(get_current_admin),
):
    if _admin['role'] == 'admin' or _admin['role'] == 'teacher':
        db_group = get_group_by_id(db, group_id)
        return Response(code=200, success=True, message="success", data=db_group).model_dump()
    else:
        raise HTTPException(status_code=422, detail="Ushbu userda bunday amalni bajarishga huquqi yo'q")

@router.delete("/delete_group/{group_id}")
async def get_group(
        group_id: uuid.UUID,
        db: Session = Depends(get_db),
        _admin=Depends(get_current_admin),
):
    if _admin['role'] == 'admin' or _admin['role'] == 'teacher':
        deleted = delete_group(db, group_id)
        if deleted == 0:
            return Response(
                code=422,
                success=False,
                message="group not found",
                data=deleted
            ).model_dump()
        else:

            return Response(
                code=200,
                success=True,
                message="deleted",
                data=deleted
            ).model_dump()
    else:
        raise HTTPException(status_code=422, detail="Ushbu userda bunday amalni bajarishga huquqi yo'q")


@router.put("/update_group")
async def update_group_route(
        # group_id: uuid.UUID,
        group: GroupsSchema,
        db: Session = Depends(get_db),
        _admin=Depends(get_current_admin),
):
    if _admin['role'] == 'admin' or _admin['role'] == 'teacher':
        _group = update_group(db, group, group.id)
        return Response(code=200, success=True, message="updated", data=_group).model_dump()
    else:
        raise HTTPException(status_code=422, detail="Ushbu userda bunday amalni bajarishga huquqi yo'q")
