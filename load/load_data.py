import os
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.user import User
from utils.logger import logger,log_execution_time


BASE_DIR = Path(__file__).resolve().parent.parent

@log_execution_time
def load_data():
    db: Session = SessionLocal()

    csv_file = os.path.join(BASE_DIR, "data", "users.csv")

    try:
        logger.info("Reading CSV file...")

        df = pd.read_csv(csv_file)

        logger.info(f"Records to load: {len(df)}")

        if len(df) == 0:
            logger.warning("CSV file contains no records to load.")

        # Clear existing data
        db.query(User).delete()

        # Insert new data
        for _, row in df.iterrows():
            user = User(
                id=int(row["id"]),
                name=row["name"],
                username=row["username"],
                email=row["email"],
                phone=row["phone"],
                website=row["website"],
            )
            db.add(user)

        db.commit()

        logger.info(f"Successfully loaded {len(df)} records into PostgreSQL.")

    except Exception as e:
        db.rollback()
        logger.error(f"Loading failed: {e}")
        raise

    finally:
        db.close()