from pydantic_settings import BaseSettings

from config._constants import ENV_FILE_PATH


class BaseConfig(BaseSettings):
    env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8877

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = "utf-8"
