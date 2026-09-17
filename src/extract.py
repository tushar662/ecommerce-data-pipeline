import pandas as pd
import os

RAW_FILE = "data/raw/olist_orders_dataset.csv"
SAMPLE_FILE = "data/sample/orders_sample.csv"

if os.path.exists(RAW_FILE):
    input_file = RAW_FILE
    print("Running with full raw dataset...")
else:
    input_file = SAMPLE_FILE
    print("Raw dataset not found. Running with sample dataset...")

orders = pd.read_csv(input_file)

print("Orders dataset loaded successfully!")
print("Input file:", input_file)
print("Total rows:", len(orders))
print("Total columns:", len(orders.columns))