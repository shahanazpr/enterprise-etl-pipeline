import logging
import os
import time
import functools

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/etl_pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("etl_pipeline")


def log_execution_time(func):
    """Decorator that logs how long a function took to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        logger.info(f"Starting '{func.__name__}'...")
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.info(f"Finished '{func.__name__}' in {elapsed:.2f}s")
            return result
        except Exception:
            elapsed = time.time() - start
            logger.error(f"'{func.__name__}' failed after {elapsed:.2f}s")
            raise
    return wrapper