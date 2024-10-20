import pytest


@pytest.mark.asyncio
async def test_foo_api(async_client):
    response = await async_client.get('api/examples/foo')
    assert response.text == 'bar'
