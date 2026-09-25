import pandas as pd
import pytest

from src.validate import validate_orders


def test_valid_orders():

    orders = pd.DataFrame({
        "order_id": ["A001", "A002", "A003"]
    })

    result = validate_orders(orders)

    assert len(result) == 3


def test_duplicate_order_id():

    orders = pd.DataFrame({
        "order_id": ["A001", "A001", "A003"]
    })

    with pytest.raises(ValueError):
        validate_orders(orders)


def test_missing_order_id():

    orders = pd.DataFrame({
        "order_id": ["A001", None, "A003"]
    })

    with pytest.raises(ValueError):
        validate_orders(orders)