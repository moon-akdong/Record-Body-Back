from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.core.dependency import verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
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

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(form_data.username, db)

    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "이메일 또는 비밀번호가 올바르지 않습니다.",
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.username},
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        email=current_user.email,
        name=current_user.username,
        birth_date=current_user.birth_date,
        gender=current_user.gender,
        height=current_user.height,
        weight=current_user.weight
    )
