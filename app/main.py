from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.user import router as user_router
from app.api.meal import router as meal_router
from app.core.config import settings
from app.core.logging import setup_logger

setup_logger()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(meal_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
