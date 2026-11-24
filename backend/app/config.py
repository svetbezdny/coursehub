from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "dev"

    app_title: str = "CourseHub API"
    app_version: str = "1.0.0"
    app_description: str = "API мини-платформы онлайн-курсов."

    secret_key: str = Field(min_length=32)
    access_token_expire_minutes: int = Field(default=30, gt=0)

    database_url: str = "sqlite+aiosqlite:///./coursehub.db"
    seed_demo_data: bool = True

    request_id_header: str = "X-Request-ID"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="COURSEHUB_",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
