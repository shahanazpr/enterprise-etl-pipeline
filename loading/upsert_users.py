import pandas as pd

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from models.user import User


def upsert_users():

    df = pd.read_csv("raw_data/cleaned_users.csv")

    session: Session = SessionLocal()

    try:
        for _, row in df.iterrows():

            existing_user = session.query(User).filter_by(
                id=row["id"]
            ).first()

            if existing_user:
                # Update existing record
                existing_user.name = row["name"]
                existing_user.username = row["username"]
                existing_user.email = row["email"]
                existing_user.phone = row["phone"]
                existing_user.website = row["website"]
                existing_user.city = row["city"]
                existing_user.zipcode = row["zipcode"]
                existing_user.company_name = row["company_name"]

            else:
                # Insert new record
                new_user = User(
                    id=row["id"],
                    name=row["name"],
                    username=row["username"],
                    email=row["email"],
                    phone=row["phone"],
                    website=row["website"],
                    city=row["city"],
                    zipcode=row["zipcode"],
                    company_name=row["company_name"]
                )

                session.add(new_user)

        session.commit()

        print("✅ Upsert completed successfully!")

    except Exception as e:
        session.rollback()
        print("❌ Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    upsert_users()