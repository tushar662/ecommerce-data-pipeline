import os
import pandas as pd


RAW_FILE = "data/raw/olist_orders_dataset.csv"
SAMPLE_FILE = "data/sample/orders_sample.csv"


def load_orders(use_sample=False):
    """
    Load the Olist orders dataset.

    Uses the sample dataset when use_sample=True.
    Otherwise, uses the full dataset when available.
    """

    if use_sample:
        input_file = SAMPLE_FILE
        print("Using sample dataset.")

    elif os.path.exists(RAW_FILE):
        input_file = RAW_FILE
        print("Using full raw dataset.")

    else:
        input_file = SAMPLE_FILE
        print("Full dataset not found. Using sample dataset.")

    orders = pd.read_csv(input_file)

    print(f"Loaded: {input_file}")
    print(f"Rows: {len(orders)}")
    print(f"Columns: {len(orders.columns)}")

    return orders


if __name__ == "__main__":
    orders = load_orders()

    print("\nOrders dataset loaded successfully.")