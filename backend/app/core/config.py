import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings.

    These settings can be configured through environment variables.
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GraphedGoal API"

    # CORS settings
    # In production, replace with specific origins
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Firebase settings
    FIREBASE_SERVICE_ACCOUNT_KEY: str = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_KEY", "")

    # Server settings
    HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    class Config:
        case_sensitive = True


settings = Settings()
