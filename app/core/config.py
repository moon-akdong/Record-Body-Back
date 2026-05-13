from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


def _get_env_file() -> str | None:
    """환경변수 파일 탐색: .env → .env.dev 순으로 우선 로딩."""
    for name in (".env.dev", ".env"):
        path = BASE_DIR / name
        if path.is_file():
            return str(path)
    return None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_get_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_user: str
    mysql_root_password: str
    db_host: str = "localhost"
    db_port: int = 3306
    mysql_database: str
    base_url: str

    redis_broker_url: str = ""
    redis_backend_url: str = ""
    redis_url: str = ""
    cors_origins: str = ""

    food_db_url: str
    food_db_key: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @computed_field # 모델 필드 처럼 포함 시킴 
    @property
    def sqlalchemy_database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.mysql_root_password}"
            f"@{self.db_host}:{self.db_port}/{self.mysql_database}"
        )

    @computed_field
    @property
    def cors_origin_list(self) -> list[str]:
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
