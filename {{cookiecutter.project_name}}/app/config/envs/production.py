from pydantic_settings import BaseSettings


class ProductionConfig(BaseSettings):
    env: str = 'production'
    reload: bool = False
    docs_url: str = None
    redoc_url: str = None
    workers: int = 8
    origins: list[str] = ['http://localhost:3000', 'http://localhost:8080']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
