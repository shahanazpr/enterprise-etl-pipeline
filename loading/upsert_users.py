from pathlib import Path
import pandas as pd

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.user import User


BASE_DIR = Path(__file__).resolve().parent.parent


def upsert_users():

    csv_file = BASE_DIR / "data" / "users.csv"

    df = pd.read_csv(csv_file)

    session: Session = SessionLocal()

    try:
        for _, row in df.iterrows():

            existing_user = session.query(User).filter_by(
                id=int(row["id"])
            ).first()

            if existing_user:
                # Update existing record
                existing_user.name = row["name"]
                existing_user.username = row["username"]
                existing_user.email = row["email"]
                existing_user.phone = row["phone"]
                existing_user.website = row["website"]

            else:
                # Insert new record
                new_user = User(
                    id=int(row["id"]),
                    name=row["name"],
                    username=row["username"],
                    email=row["email"],
                    phone=row["phone"],
                    website=row["website"],
                )

                session.add(new_user)

        session.commit()

        print("✅ Upsert completed successfully!")

    except Exception as e:
        session.rollback()
        print(f"❌ Upsert failed: {e}")
        raise

    finally:
        session.close()