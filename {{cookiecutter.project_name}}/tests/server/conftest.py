import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise

from app.server.server import app


@pytest.fixture(scope='module', autouse=True)
async def client():
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client



@pytest.fixture(autouse=True)
async def clean_db():
    """
    Фикстура для очистки базы данных перед каждым тестом, чтобы тесты были независимыми.
    """
    for model in Tortoise.apps.get("models", {}).values():
        await model.all().delete()

