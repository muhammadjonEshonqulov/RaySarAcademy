import hashlib
import bcrypt

from sqlalchemy.orm import Session

from app.api.models import Admins
from app.api.models import Students


def get_admin_from_by_login(db: Session, login: str):
    return db.query(Admins).filter(Admins.phone_number == login).first()

def get_student_from_by_login(db: Session, login: str):
    return db.query(Students).filter(Students.phone_number == login).first()
#
# def validate_password(hashed_password: str, password: str) -> bool:
#     return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
#


# def hash_password(plain_password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
#     return hashed.decode("utf-8")