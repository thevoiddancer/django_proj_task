import pytest

from budget_app.views import STARTING_BALANCE

STATS_URL = "/api/stats"
BALANCE_URL = "/api/current_balance"


@pytest.mark.django_db
def test_current_balance(auth_client, add_income, total_income):
    # Starting balance
    total_income += STARTING_BALANCE

    result = auth_client.get(BALANCE_URL)
    expected = {
        "total_income": total_income,
        "total_expense": 0,
        "current_balance": total_income,
    }

    assert result.status_code == 200
    assert result.data == expected


@pytest.mark.django_db
def test_stats(auth_client, add_income):
    result = auth_client.get(f"{STATS_URL}?date_from=2025-02-01&date_to=2025-05-01&agg=Avg")

    assert result.status_code == 200
    assert result.data["incomes"]["avg"] == 3100
