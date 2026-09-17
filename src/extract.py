import pandas as pd

RAW_FILE = "data/raw/olist_orders_dataset.csv"
SAMPLE_FILE = "data/sample/orders_sample.csv"

orders = pd.read_csv(RAW_FILE)

print("Orders dataset loaded successfully!")
print("Total rows:", len(orders))
print("Total columns:", len(orders.columns))

sample = orders.head(1000)

sample.to_csv(SAMPLE_FILE, index=False)

print("Sample dataset created successfully!")
print("Sample rows:", len(sample))
print("Sample file:", SAMPLE_FILE)