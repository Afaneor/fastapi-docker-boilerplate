from contextlib import asynccontextmanager
from typing import AsyncGenerator

from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api import router


{% if cookiecutter.use_sentry == 'yes' %}
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
{% endif %}

def _init_router(_app: FastAPI) -> None:
    _app.include_router(router)

def _init_middleware(_app: FastAPI) -> None:
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

{% if cookiecutter.use_sentry == 'yes' %}
def _init_sentry() -> None:
    if settings.use_sentry:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            integrations=[FastApiIntegration()],
            traces_sample_rate=1.0,
            environment=settings.env,
        )
{% endif %}

@asynccontextmanager
async def lifespan_test(_app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        db_url=settings.test_db_url,
        app_modules=settings.apps_for_tests,
        testing=True,
    )
    try:
        async with RegisterTortoise(
            app=_app,
            config=config,
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
    {% if cookiecutter.use_sentry == 'yes' %}
    _init_sentry()
    {% endif %}
    _app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    _init_router(_app)
    _init_middleware(_app)
    return _app

app = create_app()
