import pandas as pd

from src.transform_dates import transform_dates
from src.transform_delivery import transform_delivery


def test_transform_dates():

    data = {
        "order_purchase_timestamp": ["2018-01-01 10:00:00"],
        "order_approved_at": ["2018-01-01 11:00:00"],
        "order_delivered_carrier_date": ["2018-01-02 10:00:00"],
        "order_delivered_customer_date": ["2018-01-05 10:00:00"],
        "order_estimated_delivery_date": ["2018-01-06 10:00:00"]
    }

    orders = pd.DataFrame(data)

    result = transform_dates(orders)

    assert pd.api.types.is_datetime64_any_dtype(
        result["order_purchase_timestamp"]
    )

    assert "purchase_date" in result.columns
    assert "purchase_year" in result.columns
    assert "purchase_month" in result.columns
    assert "purchase_day" in result.columns
    assert "purchase_weekday" in result.columns

    assert result["purchase_year"].iloc[0] == 2018
    assert result["purchase_month"].iloc[0] == 1
    
def test_transform_delivery():

    data = {
        "order_status": ["delivered"],
        "order_purchase_timestamp": [
            pd.Timestamp("2018-01-01 10:00:00")
        ],
        "order_delivered_customer_date": [
            pd.Timestamp("2018-01-05 10:00:00")
        ],
        "order_estimated_delivery_date": [
            pd.Timestamp("2018-01-06 10:00:00")
        ]
    }

    orders = pd.DataFrame(data)

    result = transform_delivery(orders)

    assert result["delivery_days"].iloc[0] == 4.0
    assert result["delivery_status"].iloc[0] == "On Time"
    assert result["delivery_date_missing"].iloc[0] == False