import uuid
from fastapi import APIRouter, Depends, Request

# students/router.py
from fastapi import APIRouter, File, UploadFile
from typing import List
import os, shutil

from requests import Session

from app.api.schemas import Response
from app.api.sessians.crud import get_student_by_id
from app.api.students.crud import get_student
from app.db import get_db
from app.utils.auth_middleware import get_current_student

router = APIRouter()
UPLOAD_DIR = "my_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def create_upload_files(files: List[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_location)
    return {"saved_files": saved_files}

@router.get("/student-me")
async def get_student_by_id_route(
        db: Session = Depends(get_db),
        current_student: dict = Depends(get_current_student),
):
    _student = get_student_by_id(db, current_student["id"])
    return Response(
        code=200, success=True, message="success", data=_student
    ).model_dump()


@router.get("/get_student/{student_id}")
async def get_student_by_id_route(
        student_id: uuid.UUID,
        db: Session = Depends(get_db),
        _=Depends(get_current_student),
):
    _student = get_student_by_id(db, student_id)
    return Response(code=200, success=True, message="success", data=_student).model_dump()


#
#
@router.get("/get_students")
async def get_students_route(
        req: Request,
        db: Session = Depends(get_db),
        _=Depends(get_current_student),
):
    limit = int(req.query_params.get("results") or 10)
    skip = int(req.query_params.get("page") or 1) - 1
    debt = req.query_params.get("debt")
    _students, _count_of_students = get_student(
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
        data=_students
        ,
    ).model_dump()

#
# @router.post("/add_student")
# async def create_student_route(
#         student: StudentInfoSchema,
#         db: Session = Depends(get_db),
#         _=Depends(get_current_student),
# ):
#     message = create_student(db, student)
#     return Response(code=201, success=True, message=message).model_dump()
#
#
# @router.delete("/delete_student/{student_id}")
# async def delete_student_route(
#         student_id: uuid.UUID,
#         db: Session = Depends(get_db),
#         _=Depends(get_current_student),
# ):
#     delete_student(db, student_id)
#     return Response(
#         code=200,
#         success=True,
#         message="deleted",
#     ).model_dump()
#
#
# @router.put("/update_student/{student_id}")
# async def update_student_route(
#         student_id: uuid.UUID,
#         student: UserSchema,
#         db: Session = Depends(get_db),
#         _=Depends(get_current_student),
# ):
#     _student = update_student(db, student, student_id)
#     return Response(code=200, success=True, message="updated", data=_student).model_dump()
