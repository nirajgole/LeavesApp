from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # API Metadata
    PROJECT_NAME: str = "HR Module API"
    API_V1_STR: str = "/api/v1.0"

    # Database Settings (SQL Server)
    # Defaulting to the structure required for local SQL Server testing
    DATABASE_URL:str

    # JWT & Security
    # Default DurationInMinutes is 1440 (24 hours) as per documentation
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Documentation Settings
    # This reflects the functional areas in the HR Module [cite: 9]
    TAGS_METADATA: List[dict] = [
        {"name": "Authentication", "description": "Login and Token management"},
        {"name": "Leave Management", "description": "Full-day, Half-day leave and balances"},
        {"name": "Employee", "description": "Profile and Team data"}
    ]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()