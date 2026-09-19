import pandas as pd


def transform_orders(orders):
    """
    Perform order-level transformations and quality checks.
    """

    # Check duplicate order IDs
    duplicate_orders = orders["order_id"].duplicated().sum()

    print(f"Duplicate order IDs: {duplicate_orders}")

    # Check duplicate customer IDs
    duplicate_customers = orders["customer_id"].duplicated().sum()

    print(f"Duplicate customer IDs: {duplicate_customers}")

    # Check order status distribution
    print("\nOrder status distribution:")
    print(orders["order_status"].value_counts())

    # Check missing values
    print("\nMissing values:")
    print(orders.isnull().sum())

    return orders