from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.utils.constants import DATABASE_URL

# ✅ Engine yaratish
engine = create_engine(url=DATABASE_URL)

# ✅ SessionLocal yaratish
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# ✅ Base model yaratish (Barcha ORM modellar buni extends qiladi)
Base = declarative_base()

# ✅ Dependency - DB sessiyasini yaratish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
