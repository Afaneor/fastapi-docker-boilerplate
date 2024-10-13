from pydantic_settings import BaseSettings

from config.constants import ENV_FILE_PATH


class BaseConfig(BaseSettings):
    env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # CORS settings
    cors_origins: list[str] = ["*"]

    # Sentry settings

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = "utf-8"
