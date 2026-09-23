CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    purchase_date DATE,
    purchase_year INTEGER,
    purchase_month INTEGER,
    purchase_day INTEGER,
    purchase_weekday TEXT,
    delivery_days DOUBLE PRECISION,
    delivery_date_missing BOOLEAN,
    days_late DOUBLE PRECISION,
    delivery_status TEXT
);

CREATE INDEX IF NOT EXISTS idx_orders_status
ON orders(order_status);

CREATE INDEX IF NOT EXISTS idx_orders_purchase_date
ON orders(purchase_date);