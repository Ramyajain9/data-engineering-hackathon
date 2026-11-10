
import pandas as pd


def test_missing_values():
    data = pd.DataFrame({
        "order_id": [101, 102],
        "amount": [2000, None]
    })

    assert data["amount"].isnull().sum() == 1


def test_duplicate_orders():
    data = pd.DataFrame({
        "order_id": [101, 101, 102]
    })

    assert data["order_id"].duplicated().sum() == 1


def test_invalid_amounts():
    data = pd.DataFrame({
        "amount": [2000, -500, 0]
    })

    invalid = data[data["amount"] <= 0]

    assert len(invalid) == 2


def test_unknown_customer():
    orders = pd.DataFrame({
        "customer_id": ["C01", "C99"]
    })

    customers = pd.DataFrame({
        "customer_id": ["C01", "C02"]
    })

    unknown = orders[
        ~orders["customer_id"].isin(customers["customer_id"])
    ]

    assert len(unknown) == 1


def test_empty_orders():
    data = pd.DataFrame(
        columns=["order_id", "customer_id", "amount"]
    )

    assert data.empty
    assert len(data) == 0
