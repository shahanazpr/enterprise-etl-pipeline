import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user_model import User
from utils.logger import logger


def load_data():
    db: Session = SessionLocal()

    try:
        logger.info("Reading CSV file...")

        df = pd.read_csv("data/users.csv")

        # Clear existing data
        db.query(User).delete()

        # Insert data into PostgreSQL
        for _, row in df.iterrows():
            user = User(
                id=int(row["id"]),
                name=row["name"],
                username=row["username"],
                email=row["email"],
            )
            db.add(user)

        db.commit()

        logger.info("Data loaded into PostgreSQL successfully!")

    except Exception as e:
        db.rollback()
        logger.error(f"Loading failed: {e}")

    finally:
        db.close()
