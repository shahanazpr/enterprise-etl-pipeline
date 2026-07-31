from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    API_URL: str = "https://jsonplaceholder.typicode.com/users"

    DB_USER: str = "postgres"
    DB_PASSWORD: str = "702526"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "enterprise_etl"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()