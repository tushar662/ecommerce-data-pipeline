def transform_delivery(orders):
    """
    Perform delivery-related transformations.
    """

    # Calculate actual delivery time in days
    orders["delivery_days"] = (
        orders["order_delivered_customer_date"]
        - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Check if delivered order is missing actual delivery date
    orders["delivery_date_missing"] = (
        (orders["order_status"] == "delivered")
        & (orders["order_delivered_customer_date"].isnull())
    )

    # Calculate how many days early or late the order was
    orders["days_late"] = (
        orders["order_delivered_customer_date"]
        - orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Default status
    orders["delivery_status"] = "Unknown"

    delivered = orders["order_status"] == "delivered"

    # Delivered on or before estimated date
    orders.loc[
        delivered
        & orders["order_delivered_customer_date"].notnull()
        & (
            orders["order_delivered_customer_date"]
            <= orders["order_estimated_delivery_date"]
        ),
        "delivery_status"
    ] = "On Time"

    # Delivered after estimated date
    orders.loc[
        delivered
        & orders["order_delivered_customer_date"].notnull()
        & (
            orders["order_delivered_customer_date"]
            > orders["order_estimated_delivery_date"]
        ),
        "delivery_status"
    ] = "Late"

    return orders