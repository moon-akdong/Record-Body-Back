from sqlalchemy.orm import Session

from app.models.user import User, Gender
from app.schemas.user import UserCreate, UserUpdateBody, UserProfileUpdate
from app.core.dependency import get_password_hash

def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(user_create:UserCreate, db:Session) -> User:
    new_user = User(
        email = user_create.email,
        password=get_password_hash(user_create.password),
        username=user_create.name,
        birth_date=user_create.birth_date,
        gender=user_create.gender.value.lower(),
        height=user_create.height,
        weight=user_create.weight,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(user: User, user_update: UserUpdateBody, db: Session) -> User:
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def update_user_profile(user: User, profile: UserProfileUpdate, db: Session) -> User:
    user.username = profile.name
    user.birth_date = profile.birth_date
    user.gender = profile.gender.value.lower()
    user.height = profile.height
    user.weight = profile.weight
    db.commit()
    db.refresh(user)
    return user