

print("Ecommerce Data Pipeline Started")


from src.extract import load_orders
from src.transform_dates import transform_dates
from src.transform_orders import transform_orders
from src.transform_delivery import transform_delivery


def main():

    print("\nStarting pipeline...")

    # Step 1: Extract
    orders = load_orders()

    # Step 2: Transform dates
    orders = transform_dates(orders)

    # Step 3: Transform orders
    orders = transform_orders(orders)

    # Step 4: Transform delivery
    orders = transform_delivery(orders)

    print("\nPipeline completed successfully.")
    print("Final rows:", len(orders))
    print("Final columns:", len(orders.columns))


if __name__ == "__main__":
    main()

