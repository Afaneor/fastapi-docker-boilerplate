from pydantic_settings import BaseSettings

from config.constants import ENV_FILE_PATH


class DevelopmentConfig(BaseSettings):
    env: str = 'development'
    reload: bool = True
    workers: int = 2

    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # CORS settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    use_sentry: bool = False


    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
