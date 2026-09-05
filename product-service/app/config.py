from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "No name project"
    database_dsn: str = ""
    debug: bool = False
    summary: str = "No summary"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()