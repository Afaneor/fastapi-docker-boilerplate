from config.components.base import BaseConfig
from config.components.db import DatabaseConfig
from config.components.redis import RedisConfig


class ComponentsConfig(BaseConfig, DatabaseConfig, RedisConfig):
    pass


__all__ = ["ComponentsConfig"]