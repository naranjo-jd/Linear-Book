"""Configuration management for the application."""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./test.db"
    )
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Code execution
    SANDBOX_TIMEOUT = int(os.getenv("SANDBOX_TIMEOUT", "10"))
    MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "5000"))

settings = Settings()
