from starlette.testclient import TestClient
from server.server import app
import pytest


@pytest.fixture(scope='session')
def client() -> TestClient:
    return TestClient(app)
