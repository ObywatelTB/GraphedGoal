import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    """Application settings."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GraphedGoal API"
    PROJECT_DESCRIPTION: str = "API for goal visualization and planning"

    # CORS settings
    # In production, replace with specific origins
    BACKEND_CORS_ORIGINS: list = ["*"]

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "o3-mini")

    # Firebase settings
    FIREBASE_SERVICE_ACCOUNT_KEY: str = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_KEY", "")

    # Server settings
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    class Config:
        case_sensitive = True


# Create global settings object
settings = Settings()
