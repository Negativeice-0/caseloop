import os
from dotenv import load_dotenv

load_dotenv()

def _csv_setting(name: str, default: str) -> list[str]:
    value = os.getenv(name, default)
    return [entry.strip() for entry in value.split(",") if entry.strip()]


class Settings:
    PROJECT_NAME: str = "CaseLoop"
    VERSION: str = "0.1.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = APP_ENV != "production"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./caseloop.db")
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    CORS_ORIGINS: list[str] = _csv_setting(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    )
    SESSION_TTL_SECONDS: int = int(os.getenv("SESSION_TTL_SECONDS", "43200"))
    WHATSAPP_VERIFY_TOKEN: str | None = os.getenv("WHATSAPP_VERIFY_TOKEN")
    WHATSAPP_APP_SECRET: str | None = os.getenv("WHATSAPP_APP_SECRET")

settings = Settings()
