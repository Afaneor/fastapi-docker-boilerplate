from contextlib import asynccontextmanager
from typing import AsyncGenerator

from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from config import settings
from api import router
from fastapi import FastAPI


def _init_router(_app: FastAPI) -> None:
    _app.include_router(router)


@asynccontextmanager
async def lifespan_test(_app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        async with RegisterTortoise(
            app=_app,
            config=settings.tortoise_config,
            generate_schemas=True,
            add_exception_handlers=True,
            _create_db=True,
        ):
            yield
    except Exception as e:
        raise
    finally:
        await Tortoise._drop_databases()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        if getattr(_app.state, "testing", None):
            async with lifespan_test(_app) as _:
                yield
        else:
            async with RegisterTortoise(
                app=_app,
                config=settings.tortoise_config,
                generate_schemas=True,
                add_exception_handlers=True,
            ):
                yield
    except Exception as e:
        raise


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    _init_router(_app)
    return _app


app = create_app()
