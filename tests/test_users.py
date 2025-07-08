import pytest

@pytest.mark.django_db
def test_register_user(client):
    payload = {
        "username": "bridgekeeper",
        "password": "unladen_swallow",
        "email": "tim@bridge.com"
    }

    response = client.post('/api/register', payload)

    assert response.status_code == 201
    assert 'token' in response.data

@pytest.mark.django_db
@pytest.mark.parametrize(
    'password, code, keys',
    [
        pytest.param('unladen_swallow', 200, ['token'], id='correct pass'),
        pytest.param('wrong_pass', 400, ['non_field_errors'], id='incorrect pass'),
    ]
)
def test_get_token(client, add_user, password, code, keys):
    payload = {
        'username': 'bridgekeeper',
        'password': password,
    }

    response = client.post('/api/token', payload)

    assert response.status_code == code
    assert list(response.data.keys()) == keys

