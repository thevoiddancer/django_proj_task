import pytest

from budget_app.views import STARTING_BALANCE

API_URL = "/api/incomes"


@pytest.mark.django_db
def test_add_income(auth_client, add_categories):
    payload = {
        "title": "paycheck jan",
        "amount": 3000,
        "category": 1,
        "date": "2025-02-10",
    }
    expected_keys = list(payload.keys()) + ["id", "created_at", "updated_at", "user"]

    response = auth_client.post(API_URL, payload)

    assert response.status_code == 201
    assert response.data["id"] == 2
    assert set(response.data.keys()) == set(expected_keys)


@pytest.mark.django_db
def test_read_incomes(auth_client, add_income):
    # Starting income for a user
    incomes_num = add_income + 1
    response = auth_client.get(API_URL)

    assert response.status_code == 200
    assert len(response.data) == incomes_num


@pytest.mark.django_db
def test_read_single_income(auth_client, add_income):
    response = auth_client.get(f"{API_URL}/1")

    assert response.status_code == 200
    assert response.data["title"] == "Starting Balance"
    assert response.data["category"] is None
    assert float(response.data["amount"]) == STARTING_BALANCE

    response = auth_client.get(f"{API_URL}/2")

    assert response.status_code == 200
    assert response.data["title"] == "paycheck jan"
    assert response.data["category"] == 1
    assert float(response.data["amount"]) == 3000.00


@pytest.mark.django_db
def test_update_category(auth_client, add_income):
    payload_mod = {"title": "regres dec"}
    auth_client.patch(f"{API_URL}/6", payload_mod, format="json")

    response = auth_client.get(f"{API_URL}/6")

    assert response.status_code == 200
    assert response.data["title"] == "regres dec"


@pytest.mark.django_db
def test_delete_income(auth_client, add_income):
    # Starting balance for new user
    income_num = add_income + 1
    auth_client.delete(f"{API_URL}/2")

    response = auth_client.get(API_URL)
    assert response.status_code == 200
    assert len(response.data) == income_num - 1


@pytest.mark.django_db
def test_filter_incomes(auth_client, add_income):
    response = auth_client.get(f"{API_URL}?date_from=2025-02-01&date_to=2025-05-01")

    assert response.status_code == 200
    assert len(response.data) == 3
