from pydantic_settings import BaseSettings

from config._constants import ENV_FILE_PATH


class DevelopmentConfig(BaseSettings):
    env: str = 'development'
    reload: bool = True
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'
    workers: int = 2
    origins: list[str] = ['http://localhost:3000', 'http://localhost:8080']

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'

