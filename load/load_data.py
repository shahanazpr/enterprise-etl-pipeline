from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)


def load_data(df):
    # Read existing user IDs
    try:
        existing = pd.read_sql(
            text("SELECT id FROM users"),
            engine
        )
    except Exception:
        existing = pd.DataFrame(columns=["id"])

    # Keep only new records
    if not existing.empty:
        df = df[~df["id"].isin(existing["id"])]

    # Load only if new records exist
    if not df.empty:
        df.to_sql(
            "users",
            engine,
            if_exists="append",
            index=False
        )
        print(f"{len(df)} new records loaded into PostgreSQL.")
    else:
        print("No new records to load.")