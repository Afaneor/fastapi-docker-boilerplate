import pytest


@pytest.mark.asyncio
async def test_foo_api_en(async_client):
    response = await async_client.get(
        'api/examples/foo',
        headers={'Accept-Language': 'en;q=0.8,'}
    )
    assert response.text == 'bar'

@pytest.mark.asyncio
async def test_foo_api_ru(async_client):
    response = await async_client.get(
        'api/examples/foo',
        headers={'Accept-Language': 'ru;q=0.8,'}
    )
    assert response.text == 'бар'

@pytest.mark.asyncio
async def test_pydantic_validation_error_en(async_client):
    response = await async_client.post(
        'api/examples/foo',
        json={}
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Field required'

@pytest.mark.asyncio
async def test_pydantic_validation_error_with_locale(async_client):
    response = await async_client.post(
        'api/examples/foo',
        headers={'Accept-Language': 'ru;q=0.8,'},
        json={}
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Обязательное поле'

@pytest.mark.asyncio
async def test_pagination(async_client):
    response = await async_client.get(
        'api/examples/a-lot-of-data?page=1&size=10',
    )
    assert response.status_code == 200
    assert response.json()['total'] == 1000
    assert response.json()['items'][0]['foo'] == '0'
    assert response.json()['items'][-1]['foo'] == '9'
