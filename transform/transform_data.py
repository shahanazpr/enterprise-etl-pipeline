import os
from pathlib import Path
import pandas as pd

from utils.logger import logger,log_execution_time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@log_execution_time
def transform_data():
     # Ensure the data directory exists
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    input_file = os.path.join(BASE_DIR, "data", "users.json")
    output_file = os.path.join(BASE_DIR, "data", "users.csv")

    try:
        logger.info("Reading JSON file...")

        df = pd.read_json(input_file)

        logger.info(f"Records before cleaning: {len(df)}")

        if len(df) == 0:
            logger.warning("No records found in input file — nothing to transform.")

        # Remove duplicate records
        before = len(df)
        df.drop_duplicates(subset=["id"], inplace=True)
        removed = before - len(df)
        if removed > 0:
            logger.warning(f"Removed {removed} duplicate record(s).")

        # Remove leading/trailing spaces
        df["name"] = df["name"].str.strip()
        df["username"] = df["username"].str.strip()
        df["email"] = df["email"].str.strip()

        # Standardize text
        df["name"] = df["name"].str.title()
        df["email"] = df["email"].str.lower()

        # Keep only required columns
        df = df[
            [
                "id",
                "name",
                "username",
                "email",
                "phone",
                "website",
            ]
        ]

        df.to_csv(output_file, index=False)

        logger.info(f"Transformation completed successfully.")
        logger.info(f"CSV saved at: {output_file}")
        logger.info(f"Records after cleaning: {len(df)}")

    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise