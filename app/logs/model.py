from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime
from app.db import Base
from app.db import engine


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, nullable=False)
    url = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    processing_time = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    request_body = Column(Text, nullable=True)
    response_body = Column(Text, nullable=True)
    headers = Column(Text, nullable=True)

    # ✅ Yangi qo‘shilgan maydon
    user_id = Column(String, nullable=True)  # Foydalanuvchi ID yoki email (agar mavjud bo‘lsa)

Base.metadata.create_all(bind=engine)
