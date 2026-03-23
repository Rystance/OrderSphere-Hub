from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent


class Settings(BaseSettings):
    app_name: str = "OrderSphere-Hub"
    backend_cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    database_url: str = f"sqlite:///{ROOT_DIR / 'db' / 'ordersphere.db'}"

    # JWT 相关
    secret_key: str = "CHANGE_ME_SECRET_KEY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 天

    # 管理员注册密钥
    admin_secret: str = "CHANGE_ME_ADMIN_SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
