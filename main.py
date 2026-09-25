from src.logger import get_logger

logger = get_logger()

logger.info("Ecommerce Data Pipeline Started")

from src.extract import load_orders as extract_orders
from src.transform_dates import transform_dates
from src.transform_orders import transform_orders
from src.transform_delivery import transform_delivery
from src.validate import validate_orders
from src.load import load_orders as load_to_database


def main():

    try:

        logger.info("Starting pipeline")

        # Step 1: Extract
        logger.info("Starting extraction")
        orders = extract_orders(use_sample=True)
        logger.info("Extraction completed")

        # Step 2: Transform dates
        logger.info("Starting date transformation")
        orders = transform_dates(orders)
        logger.info("Date transformation completed")

        # Step 3: Transform orders
        logger.info("Starting order transformation")
        orders = transform_orders(orders)
        logger.info("Order transformation completed")

        # Step 4: Transform delivery
        logger.info("Starting delivery transformation")
        orders = transform_delivery(orders)
        logger.info("Delivery transformation completed")

        # Step 5: Validate data
        logger.info("Starting data validation")
        orders = validate_orders(orders)
        logger.info("Data validation completed")

        # Step 6: Load into PostgreSQL
        logger.info("Starting database load")
        load_to_database(orders)
        logger.info("Database load completed")

        logger.info("Pipeline completed successfully")
        logger.info(f"Final rows: {len(orders)}")
        logger.info(f"Final columns: {len(orders.columns)}")

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    main()