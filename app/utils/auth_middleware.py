from datetime import timedelta, datetime

# import jwt
from jose import jwt, JWTError

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.utils.constants import SECRET_KEY, ALGORITHM

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth3_scheme = OAuth2PasswordBearer(tokenUrl="auth/student_login")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        staff_id: str = payload.get("id")
        role: str = payload.get("role")
        if staff_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": staff_id, "role": role}
    # except PyJWTError:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_admin(token: str = Depends(oauth3_scheme)):
    admin = decode_access_token(token)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": admin["id"], "role": admin["role"]}

def get_current_student(token: str = Depends(oauth2_scheme)):
    student = decode_access_token(token)
    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": student["id"], "role": student["role"]}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # JWT token ichidan foydalanuvchi ID ni olish
        if user_id is None:
            return "Anonymous"
        return user_id
    except JWTError:
        return "Anonymous e"

def get_current_user_from_request(authorization: str):
    """Request headerdan JWT tokenni olib, foydalanuvchini aniqlash."""
    if not authorization:
        return "Anonymous"

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # JWT token ichidan foydalanuvchi ID ni olish
        return user_id if user_id else "Anonymous"

    except JWTError:
        return "Anonymous"
