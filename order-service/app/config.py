from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    project_name: str = "No name project"
    summary: str = "No summary"

    database_dsn: str = ""
    database_dsn_local: str = ""

    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    is_local: bool = True
    debug: bool = False

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")


settings = Settings()