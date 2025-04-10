from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import ENV_FILE_PATH


class DatabaseConfig(BaseSettings):
    postgres_host: str = Field(default='localhost')
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default='postgres')
    postgres_password: str = Field(default='postgres')
    postgres_db: str = Field(default='postgres')
    postgres_dsn: str = Field(default='')
    test_db_url: str = Field(default='sqlite://:memory:')

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
    )

    @computed_field(return_type=str)
    def postgres_connection_string(self):
        return self.postgres_dsn or f'postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    @computed_field(return_type=dict)
    def tortoise_config(self):
        return {
            'connections': {
                'default': self.postgres_connection_string
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

    @computed_field(return_type=dict)
    def apps_for_tests(self):
        app_modules = {}

        # Iterate through the apps in the original Tortoise config
        for app_name, app_config in self.tortoise_config['apps'].items():
            # Filter out `aerich.models` and prefix with `app.`
            test_models = [
                f"app.{model}" if not model.startswith('app.') else model
                for model in app_config['models']
                if model != 'aerich.models'
            ]

            # Only include apps that have valid models after filtering
            if test_models:
                app_modules[app_name] = test_models

        return app_modules
