from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    database_dsn: str = ""
    database_dsn_local: str = ""

    is_local: bool = True

    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    tortoise_orm: str = ""

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")


settings = Settings()