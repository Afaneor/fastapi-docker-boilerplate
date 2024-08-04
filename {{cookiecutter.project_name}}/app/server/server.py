from config import settings
from api import router
from fastapi import FastAPI


def _init_router(_app: FastAPI) -> None:
    _app.include_router(router)


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    _init_router(_app)
    return _app


app = create_app()
