from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
import os

# Always resolve .env relative to this file (backend/.env), not the CWD
_ENV_PATH = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # LLM
    MISTRAL_API_KEY: str = ""

    # Search
    TAVILY_API_KEY: str = ""

    # GitHub
    GITHUB_TOKEN: str = ""

    class Config:
        env_file = str(_ENV_PATH)
        env_file_encoding = "utf-8"


settings = Settings()
