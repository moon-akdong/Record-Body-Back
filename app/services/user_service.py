from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.dependencies import create_access_token, hash_password, verify_password

def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(user_create:UserCreate, db:Session) -> User:
    new_user = User(
        email = user_create.email,
        password=hash_password(user_create.password),
        username=user_create.name,
        birth_date=user_create.birth_date,
        gender=user_create.gender,
        height=user_create.height,
        weight=user_create.weight,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user