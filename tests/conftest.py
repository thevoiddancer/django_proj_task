import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


# User fixtures
@pytest.fixture
def user():
    payload = {
        "username": "bridgekeeper",
        "password": "unladen_swallow",
        "email": "tim@bridge.com",
    }
    return payload


@pytest.fixture
def add_user(client, user):
    result = client.post("/api/register", user)
    return result.data["token"]


@pytest.fixture
def auth_client(client, add_user):
    client.credentials(HTTP_AUTHORIZATION=f"Token {add_user}")
    return client


# Category fixtures
@pytest.fixture
def categories():
    payloads = [
        {"title": "paycheck", "type": "income"},
        {"title": "utilities", "type": "expense"},
        {"title": "food", "type": "expense"},
        {"title": "bonus", "type": "income", "parent": 1},
        {"title": "power", "type": "expense", "parent": 2},
        {"title": "water", "type": "expense", "parent": 2},
        {"title": "meat", "type": "expense", "parent": 3},
        {"title": "fruits", "type": "expense", "parent": 3},
    ]
    return payloads


@pytest.fixture
def add_categories(auth_client, categories):
    for category in categories:
        auth_client.post("/api/categories", category)
    return len(categories)


# Income fixtures
@pytest.fixture
def incomes():
    payloads = [
        {"title": "paycheck jan", "amount": 3000, "category": 1, "date": "2025-02-10"},
        {"title": "paycheck feb", "amount": 3100, "category": 1, "date": "2025-03-11"},
        {"title": "paycheck mar", "amount": 3200, "category": 1, "date": "2025-04-12"},
        {"title": "paycheck apr", "amount": 3300, "category": 1, "date": "2025-05-13"},
        {"title": "bonus 1", "amount": 200, "category": 4, "date": "2024-12-20"},
        {"title": "bonus 2", "amount": 220, "category": 4, "date": "2025-07-10"},
    ]
    return payloads


@pytest.fixture
def add_income(auth_client, add_categories, incomes):
    for income in incomes:
        auth_client.post("/api/incomes", income)
    return len(incomes)


@pytest.fixture
def total_income(incomes):
    income = sum([inc["amount"] for inc in incomes])
    return income
