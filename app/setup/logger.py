import logging
import sys


def configure_logging():
    formatter = logging.Formatter(
        fmt="[%(asctime)s] - [%(levelname)s] - [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    for noisy_logger in (
            "botocore.credentials",
            "botocore.auth",
            "boto3",
            "boto3.resources",
            "aiobotocore.credentials",
            "aiobotocore.client",
            "aiobotocore.endpoint",
    ):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
        logging.getLogger(noisy_logger).propagate = False
        logging.getLogger(noisy_logger).handlers.clear()

    for uvicorn_logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(uvicorn_logger_name)
        logger.handlers.clear()
        logger.propagate = True
