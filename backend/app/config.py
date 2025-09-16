"""Application configuration powered by pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration object for the backend service."""

    api_v1_prefix: str = "/api/v1"
    project_name: str = "Admin Automation Dashboard Pro"
    telemetry_interval_seconds: float = 2.0
    metrics_retention: int = 720
    logs_retention: int = 720
    notifications_retention: int = 200
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    access_token_ttl_minutes: int = 120

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AADP_", extra="ignore")


def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()


settings = get_settings()
