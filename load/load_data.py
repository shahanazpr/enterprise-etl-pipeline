import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from utils.logger import logger, log_execution_time


@log_execution_time
def load_data(df: pd.DataFrame):
    db: Session = SessionLocal()

    try:
        logger.info("Starting incremental data loading...")

        if df is None or df.empty:
            logger.warning("No records received for loading.")
            return

        logger.info(
            f"Records received for incremental loading: {len(df)}"
        )

        inserted = 0
        updated = 0
        skipped = 0

        for _, row in df.iterrows():
            try:
                user_id = int(row["id"])

                existing_user = (
                    db.query(User)
                    .filter(User.id == user_id)
                    .first()
                )

                if existing_user:
                    existing_user.name = row["name"]
                    existing_user.username = row["username"]
                    existing_user.email = row["email"]
                    existing_user.phone = row["phone"]
                    existing_user.website = row["website"]

                    updated += 1

                else:
                    new_user = User(
                        id=user_id,
                        name=row["name"],
                        username=row["username"],
                        email=row["email"],
                        phone=row["phone"],
                        website=row["website"],
                    )

                    db.add(new_user)
                    inserted += 1

            except Exception as e:
                skipped += 1

                logger.error(
                    f"Skipping record {row.get('id', 'Unknown')}: {e}"
                )

        db.commit()

        logger.info(
            "Incremental loading completed: "
            f"{inserted} inserted, "
            f"{updated} updated, "
            f"{skipped} skipped."
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Loading failed: {e}")
        raise

    finally:
        db.close()
