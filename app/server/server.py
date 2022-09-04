from fastapi import FastAPI
import config
from api import router


def _init_router(_app: FastAPI) -> None:
    _app.include_router(router)


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
    )
    _init_router(_app)
    return _app


app = create_app()
