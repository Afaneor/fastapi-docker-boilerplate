from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

ClientManagerType = AsyncGenerator[AsyncClient, None]


@asynccontextmanager
async def client_manager(app, base_url="http://test", **kw) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c
