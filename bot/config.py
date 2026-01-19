from pydantic_settings import BaseSettings

class BotSettings(BaseSettings):
    BOT_TOKEN: str = ""
    API_URL: str = "http://backend:8000/api/v1"
    WEB_APP_URL: str = "https://yourdomain.com"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = BotSettings()
