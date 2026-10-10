from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):

    services: dict = {
        "products": "http://product-service:8001"
    }

    request_timeout: float = 30.0
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")


settings = Settings()