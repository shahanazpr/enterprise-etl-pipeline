import pandas as pd
from utils.logger import logger


def transform_data():
    logger.info("Reading JSON file...")

    # Read JSON file
    df = pd.read_json("data/users.json")

    logger.info(f"Rows loaded: {len(df)}")

    # Convert JSON to CSV
    df.to_csv("data/users.csv", index=False)

    logger.info("CSV created successfully!")

    return df