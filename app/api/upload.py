from pathlib import Path
from uuid import uuid4
from fastapi import Depends
from datetime import datetime

from fastapi import APIRouter, File, HTTPException, UploadFile
from app.schemas.meal import MealImageResponse
from app.models.user import User
from app.core.config import settings
from app.core.security import get_current_user

router = APIRouter(prefix="/upload", tags=["upload"])

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR_FOOD =  UPLOAD_DIR / "food" 
UPLOAD_USER = UPLOAD_DIR / "users"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

@router.post("/image",response_model=MealImageResponse)
async def upload_image(
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...)):
    
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 이미지 형식입니다.")
    now = datetime.now()
    upload_dir_food = (
        UPLOAD_DIR_FOOD 
        / now.strftime("%Y") 
        / now.strftime("%m") 
        / now.strftime("%d") 
        / str(current_user.id)
    )
    upload_dir_food.mkdir(parents=True, exist_ok=True)

    saved_filename = f"{uuid4().hex}{extension}" # 32자리 16진수 문자열 반환 -> 파일명 중복 방지
    saved_path = upload_dir_food / saved_filename

    file_bytes = await file.read()
    saved_path.write_bytes(file_bytes)
    image_url = (
        f"{settings.base_url}uploads/food/"
        f"{now.strftime('%Y')}/{now.strftime('%m')}/{now.strftime('%d')}/"
        f"{current_user.id}/{saved_filename}"
    )
    return {
        "file_name": saved_filename,
        "image_url": image_url,
        "message": "이미지 업로드가 완료되었습니다.",
    }

@router.post("/profile_img",response_model=MealImageResponse)
async def upload_image(
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 이미지 형식입니다.")
    
    upload_users = (
        UPLOAD_DIR_FOOD 
        / str(current_user.id)
    )
    upload_users.mkdir(parents=True, exist_ok=True)
    saved_filename = f"{uuid4().hex}{extension}" # 32자리 16진수 문자열 반환 -> 파일명 중복 방지
    saved_path = upload_users / saved_filename
    file_bytes = await file.read()
    saved_path.write_bytes(file_bytes)

    image_url = (
        f"{settings.base_url}uploads/users/"
        f"{current_user.id}/{saved_filename}"
    )
    return {
        "file_name": saved_filename,
        "image_url": image_url,
        "message": "이미지 업로드가 완료되었습니다.",
    }