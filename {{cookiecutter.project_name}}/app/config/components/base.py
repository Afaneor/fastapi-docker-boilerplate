from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
