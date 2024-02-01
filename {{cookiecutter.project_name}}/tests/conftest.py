import pytest
from starlette.testclient import TestClient

from app.server.server import app


@pytest.fixture(scope='session')
def client() -> TestClient:
    return TestClient(app)
