import pandas as pd


DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]


def transform_dates(orders):
    """
    Convert order date columns into datetime
    and create useful purchase date dimensions.
    """

    # Convert string date columns to datetime
    for column in DATE_COLUMNS:
        orders[column] = pd.to_datetime(orders[column])

    # Create purchase date dimensions
    orders["purchase_date"] = orders["order_purchase_timestamp"].dt.date
    orders["purchase_year"] = orders["order_purchase_timestamp"].dt.year
    orders["purchase_month"] = orders["order_purchase_timestamp"].dt.month
    orders["purchase_day"] = orders["order_purchase_timestamp"].dt.day
    orders["purchase_weekday"] = orders["order_purchase_timestamp"].dt.day_name()

    return orders