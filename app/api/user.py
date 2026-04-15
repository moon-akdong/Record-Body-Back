from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.services.user_service import get_user, create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
def register(user_create:UserCreate,db:Session=Depends(get_db)):
    existing_user = get_user(user_create.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 이메일입니다.",
        )
    new_user = create_user(user_create,db)

    return {
        "email" : new_user.email,
    }

    