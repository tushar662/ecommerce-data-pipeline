import logging


def get_logger(name="ecommerce_pipeline"):

    logger = logging.getLogger(name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            "pipeline.log",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger