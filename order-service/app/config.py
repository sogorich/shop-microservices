from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    project_name: str = "No name project"
    database_dsn: str = ""
    debug: bool = False
    summary: str = "No summary"

    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")


settings = Settings()