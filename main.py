print("Ecommerce Data Pipeline Started")


from src.extract import load_orders as extract_orders
from src.transform_dates import transform_dates
from src.transform_orders import transform_orders
from src.transform_delivery import transform_delivery
from src.load import load_orders as load_to_database


def main():

    print("\nStarting pipeline...")

    # Step 1: Extract
    orders = extract_orders(use_sample=True)

    # Step 2: Transform dates
    orders = transform_dates(orders)

    # Step 3: Transform orders
    orders = transform_orders(orders)

    # Step 4: Transform delivery
    orders = transform_delivery(orders)

    # Step 5: Load into PostgreSQL
    load_to_database(orders)

    print("\nPipeline completed successfully.")
    print("Final rows:", len(orders))
    print("Final columns:", len(orders.columns))

if __name__ == "__main__":
    main()