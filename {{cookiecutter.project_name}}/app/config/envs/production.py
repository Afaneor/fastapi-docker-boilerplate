from pydantic_settings import BaseSettings

from config.constants import ENV_FILE_PATH


class ProductionConfig(BaseSettings):
    env: str = 'production'
    reload: bool = False
    docs_url: str = None
    redoc_url: str = None
    workers: int = 8
    origins: list[str] = ['http://localhost:3000', 'http://localhost:8080']

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
