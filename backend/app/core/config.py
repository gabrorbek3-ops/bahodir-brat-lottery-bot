from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Bahodir Brat Lottery"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/lottery_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBHOOK_URL: str = ""
    ADMIN_TELEGRAM_IDS: List[int] = []
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # File upload
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    
    # Payment
    RUS_CARD_PREFIXES: List[str] = ["2200", "2201", "2202", "2203", "2204"]
    DEFAULT_CURRENCY: str = "RUB"
    
    # Lottery
    MIN_PARTICIPANTS: int = 10
    DEFAULT_PRIZE: str = "iPhone 15 Pro"
    
    # YouTube
    YOUTUBE_API_KEY: Optional[str] = None
    YOUTUBE_CHANNEL_ID: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
