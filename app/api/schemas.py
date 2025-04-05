import uuid
from datetime import datetime
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar("T")


class StudentSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    surname: str = None
    phone_number: str
    group_id: str = None
    password: str
    role: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None

class UserTempSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = None
    surname: str = None
    phone_number: str = None
    password: Optional[str] = None
    role: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None


class AdminsSchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    surname: str = None
    password: Optional[str] = None
    phone_number: str = None
    role: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None

class GroupsSchema(BaseModel):
    id: uuid.UUID = None
    name: str = None
    science_name: str = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Response(BaseModel, Generic[T]):
    code: int
    success: bool
    message: str
    data: Optional[T] = None


class LoginSchema(BaseModel):
    login: str
    password: str
