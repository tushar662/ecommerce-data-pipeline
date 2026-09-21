import os
import psycopg


def connect_database():

    connection = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="ecommerce_db",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )

    print("PostgreSQL connection successful!")

    return connection


def load_orders(orders):

    connection = connect_database()
    cursor = connection.cursor()

    print(f"Loading {len(orders)} rows into PostgreSQL...")

    insert_query = """
        INSERT INTO orders (
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp,
            order_approved_at,
            order_delivered_carrier_date,
            order_delivered_customer_date,
            order_estimated_delivery_date,
            purchase_date,
            purchase_year,
            purchase_month,
            purchase_day,
            purchase_weekday,
            delivery_days,
            delivery_date_missing,
            days_late,
            delivery_status
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    rows = [tuple(row) for _, row in orders.iterrows()]

    cursor.executemany(insert_query, rows)

    connection.commit()

    print(f"Successfully loaded {len(rows)} rows.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    connection = connect_database()
    connection.close()