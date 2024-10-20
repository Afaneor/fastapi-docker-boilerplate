from pydantic_settings import BaseSettings

from config.constants import ENV_FILE_PATH


class ProductionConfig(BaseSettings):
    env: str = 'production'
    reload: bool = False
    workers: int = 8

    docs_url: str | None = None
    redoc_url: str | None = None

    # CORS settings
    cors_origins: list[str] = ["{{cookiecutter.production_domain}}"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    cors_allow_headers: list[str] = ["*"]

    {% if cookiecutter.use_sentry == 'yes' %}
    # Sentry settings
    use_sentry: bool = True
    sentry_dsn: str = "{{ cookiecutter.sentry_dsn }}"
    {% endif %}

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
