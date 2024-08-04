from pydantic_settings import BaseSettings


class DevelopmentConfig(BaseSettings):
    env: str = 'development'
    reload: bool = True
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'
    workers: int = 2

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

