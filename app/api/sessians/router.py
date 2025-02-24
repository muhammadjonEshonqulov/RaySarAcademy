# import uuid
# from fastapi import APIRouter, Depends, Request

# students/router.py
from fastapi import APIRouter, File, UploadFile
from typing import List
import os, shutil

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