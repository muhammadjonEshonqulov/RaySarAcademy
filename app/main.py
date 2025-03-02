import uuid

import uvicorn
import json
import time
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.db import SessionLocal
from app.logs.crud import create_request_log
from app.api.auth.router import router as auth_router
from app.api.admins.router import router as staff_router
from app.api.students.router import router as student_router
from app.utils.auth_middleware import get_current_user, decode_access_token, oauth2_scheme

app = FastAPI(title="RaySarAcademy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    db = SessionLocal()

    try:

        client_ip = request.client.host if request.client else "Unknown"
        user_agent = request.headers.get("User-Agent", "Unknown")

        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""
        if not token:
            user = {"id": 'Anonymous'}
        else:
            user =  decode_access_token(token)
        request_body = None
        if request.method in ["POST", "PUT"]:
            try:
                request_body_bytes = await request.body()
                request_body = request_body_bytes.decode("utf-8") if request_body_bytes else None
            except Exception:
                request_body = None

        headers = json.dumps(dict(request.headers))

        response = await call_next(request)

        response_content = b""
        async for chunk in response.body_iterator:
            response_content += chunk
        response_body = response_content.decode("utf-8") if response_content else None

        response = Response(
            content=response_content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )

        create_request_log(
            db=db,
            method=request.method,
            url=str(request.url.path),
            status_code=response.status_code,
            processing_time=time.time() - start_time,
            ip_address=client_ip,
            user_agent=user_agent,
            request_body=request_body,
            response_body=response_body,
            headers=headers,
            user_id=user["id"]
        )

        return response
    finally:
        db.close()


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(staff_router, prefix="/admin", tags=["Admins"])
app.include_router(student_router, prefix="/student", tags=["Student"])

from mangum import Mangum
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
