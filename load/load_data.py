import os
import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from utils.logger import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    db: Session = SessionLocal()

    csv_file = os.path.join(BASE_DIR, "data", "users.csv")

    try:
        logger.info("Reading CSV file...")

        df = pd.read_csv(csv_file)

        logger.info(f"Records to load: {len(df)}")

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