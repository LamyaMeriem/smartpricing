"""Configuration for SmartPricing Engine"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@postgres:5432/smartpricing"

    # Redis
    redis_url: str = "redis://:redis123@redis:6379/0"

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Environment
    environment: str = "development"
    log_level: str = "INFO"

    model_config = ConfigDict(
        env_file=".env.local", case_sensitive=False, extra="ignore"  # 👈 Important! Ignore les extra fields du .env
    )


settings = Settings()
