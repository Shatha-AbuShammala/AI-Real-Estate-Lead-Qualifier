from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "AI Real Estate Lead Qualifier"
    ENV: str = "development"
    DEBUG: bool = True

    # --- Database ---
    DATABASE_URL: str

    # --- Redis / Celery ---
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # --- Twilio (WhatsApp) ---
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""

    # --- Claude API ---
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-haiku-4-5-20251001"

    # --- Business logic ---
    MAX_QUALIFICATION_QUESTIONS: int = 5

    # --- Security ---
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()