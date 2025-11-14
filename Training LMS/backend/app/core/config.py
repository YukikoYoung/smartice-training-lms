from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """应用配置"""
    APP_NAME: str = "SmartIce培训管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # 数据库
    DATABASE_URL: str = "sqlite:///./training_lms.db"

    # JWT认证配置
    SECRET_KEY: str  # 必须在.env中配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 默认7天

    # 文件上传
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
