import datetime
import uuid

from sqlalchemy import Column, UUID, String, DateTime

from app.db import Base, engine


class UsersTemp(Base):
    __tablename__ = "users_temp"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True)
    name = Column(String, index=True, nullable=True)
    surname = Column(String, index=True, nullable=True)
    password = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

class Students(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True)
    name = Column(String, index=True, nullable=True)
    surname = Column(String, index=True, nullable=True)
    password = Column(String, nullable=True)
    group_id = Column(String, nullable=True)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

class Groups(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=True)
    science_name = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

class Admins(Base):
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    password = Column(String, nullable=True)
    phone_number = Column(String, unique=True)
    role = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)


Base.metadata.create_all(bind=engine)
