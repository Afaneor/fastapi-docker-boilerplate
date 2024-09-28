from config.components import ComponentsConfig
from config.envs.development import DevelopmentConfig
from config.envs.production import ProductionConfig


class ProductionSettings(ComponentsConfig, ProductionConfig):
    ...


class DevelopmentSettings(ComponentsConfig, DevelopmentConfig):
    ...


def get_settings() -> ProductionSettings | DevelopmentSettings:
    env = ComponentsConfig().env
    if env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Unknown environment: {env}")


settings = get_settings()
tortoise_settings = settings.tortoise_config  # we need this for aerich
