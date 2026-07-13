import pandas as pd
from utils.logger import logger


def transform_data():
    logger.info("Reading JSON file...")

    # Read JSON file
    df = pd.read_json("data/users.json")

    logger.info(f"Rows loaded: {len(df)}")

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove extra spaces
    df["name"] = df["name"].str.strip()
    df["username"] = df["username"].str.strip()
    df["email"] = df["email"].str.strip()

    # Standardize text
    df["name"] = df["name"].str.title()
    df["email"] = df["email"].str.lower()

    # Save transformed data
    df.to_csv("data/users.csv", index=False)

    logger.info("Data transformed and CSV created successfully!")