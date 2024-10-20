import pytest
from starlette.testclient import TestClient

from app.server.server import app


@pytest.fixture(scope='session', autouse=True)
def client() -> TestClient:
    """
    Фикстура для тестирования API.
    """
    with TestClient(app) as c:
        yield c
