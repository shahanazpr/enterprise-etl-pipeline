import sqlite3
import pandas as pd
from utils.logger import logger


def load_data():
    try:
        logger.info("Reading CSV file...")

        df = pd.read_csv("data/users.csv")

        conn = sqlite3.connect("data/users.db")

        df.to_sql("users", conn, if_exists="replace", index=False)

        conn.close()

        logger.info("Data loaded into SQLite successfully!")

    except Exception as e:
        logger.error(f"Loading failed: {e}")