from pathlib import Path
from uuid import uuid4
from fastapi import Request

from fastapi import APIRouter, File, HTTPException, UploadFile
from app.schemas.meal import MealImageResponse


router = APIRouter(prefix="/upload", tags=["upload"])

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@router.post("/image",response_model=MealImageResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...)):
    
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="지원하지 않는 이미지 형식입니다.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    saved_filename = f"{uuid4().hex}{extension}" # 32자리 16진수 문자열 반환 -> 파일명 중복 방지
    saved_path = UPLOAD_DIR / saved_filename

    file_bytes = await file.read()
    saved_path.write_bytes(file_bytes)

    return {
        "file_name": saved_filename,
        "image_url": f"{request.base_url}uploads/{saved_filename}",
        "message": "이미지 업로드가 완료되었습니다.",
    }
