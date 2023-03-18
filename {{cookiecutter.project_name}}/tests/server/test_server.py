def test_foo_api(client):
    response = client.get('api/examples/foo')
    assert response.text == 'bar'
