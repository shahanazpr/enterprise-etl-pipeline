import os
import pandas as pd

from utils.logger import logger

BASE_DIR = "/opt/airflow/project"


def transform_data():

    input_file = os.path.join(BASE_DIR, "data", "users.json")
    output_file = os.path.join(BASE_DIR, "data", "users.csv")

    try:
        logger.info("Reading JSON file...")

        df = pd.read_json(input_file)

        logger.info(f"Records before cleaning: {len(df)}")

        # Remove duplicate records
        df.drop_duplicates(subset=["id"], inplace=True)

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