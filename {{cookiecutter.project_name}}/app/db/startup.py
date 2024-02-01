import config
from tortoise import Tortoise


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(config=config.DB_CONFIG)
    # Generate the schema
    await Tortoise.generate_schemas()
