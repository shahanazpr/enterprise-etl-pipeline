import pandas as pd
from sqlalchemy import create_engine

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

# Create database connection
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Read cleaned CSV
df = pd.read_csv("raw_data/cleaned_users.csv")

# Load data into PostgreSQL
df.to_sql(
    "users",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Data loaded successfully into PostgreSQL!")