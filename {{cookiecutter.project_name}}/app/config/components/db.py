from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

from config.constants import ENV_FILE_PATH


class DatabaseConfig(BaseSettings):
    postgres_host: str = Field(default='localhost')
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default='postgres')
    postgres_password: str = Field(default='postgres')
    postgres_db: str = Field(default='postgres')
    postgres_dsn: str = Field(default='')

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'

    @computed_field(return_type=str)
    def postgres_connection_string(self):
        return self.postgres_dsn or f'postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    @computed_field(return_type=dict)
    def tortoise_config(self):
        return {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'dsn': self.postgres_connection_string
                    },
                },
            },
            'apps': {
                'server': {
                    'models': [
                        'aerich.models',
                        'db.models',
                    ],
                }
            },
        }