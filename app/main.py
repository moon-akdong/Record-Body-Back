from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.user import router as user_router
from app.api.meal import router as meal_router
from app.api.upload import router as upload_router
from app.core.config import settings
from app.core.logging import setup_logger
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)
setup_logger()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(meal_router)
app.include_router(upload_router)

BASE_DIR = Path(__file__).resolve().parent.parent  # 00_nutrients_proj/
app.mount("/uploads", StaticFiles(directory=BASE_DIR / "uploads"), name="uploads")

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
