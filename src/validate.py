def validate_orders(orders):
    """
    Validate critical order-level data.
    """

    if orders["order_id"].isnull().any():
        raise ValueError("Validation failed: order_id contains null values.")

    if orders["order_id"].duplicated().any():
        raise ValueError("Validation failed: duplicate order_id found.")

    return orders