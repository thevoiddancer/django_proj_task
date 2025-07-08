import pytest

API_URL = '/api/categories'


@pytest.mark.django_db
def test_add_category(auth_client):
    payload = {"title": "paycheck", "type": "income"}
    expected = {**payload, **{'id': 1, 'parent': None}}

    response = auth_client.post(API_URL, payload)

    assert response.status_code == 201
    assert response.data == expected


@pytest.mark.django_db
def test_read_categories(auth_client, add_categories):
    categories_num = add_categories
    response = auth_client.get(API_URL)

    assert response.status_code == 200
    assert len(response.data) == categories_num


@pytest.mark.django_db
def test_read_single_category(auth_client, add_categories):
    response = auth_client.get(f'{API_URL}/1')

    assert response.status_code == 200
    assert response.data['title'] == 'paycheck'
    assert response.data['parent'] == None

    response = auth_client.get(f'{API_URL}/4')

    assert response.status_code == 200
    assert response.data['title'] == 'bonus'
    assert response.data['parent'] == 1


@pytest.mark.django_db
def test_update_category(auth_client, add_categories):
    payload_mod = {'title': 'regres'}
    auth_client.patch(f'{API_URL}/4', payload_mod)

    response = auth_client.get(f'{API_URL}/4')

    assert response.status_code == 200
    assert response.data['title'] == 'regres'
    assert response.data['parent'] == 1


@pytest.mark.django_db
def test_delete_category(auth_client, add_categories):
    categories_num = add_categories
    auth_client.delete(f'{API_URL}/8')

    response = auth_client.get(API_URL)
    assert response.status_code == 200
    assert len(response.data) == categories_num - 1

    auth_client.delete(f'{API_URL}/1')

    response = auth_client.get(API_URL)
    assert response.status_code == 200
    assert len(response.data) == categories_num - 1 - 2
