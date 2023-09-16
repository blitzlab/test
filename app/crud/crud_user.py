from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import get_password_hash, verify_password


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create(db: Session, obj_in: UserCreate):
    hashed_password = get_password_hash(obj_in.password)
    db_user = User(email=obj_in.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session, email: str, password: str):
    user = get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user