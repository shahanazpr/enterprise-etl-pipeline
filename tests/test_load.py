import os
import pandas as pd

from load.load_data import load_data
from database import engine, SessionLocal
from models.user_model import Base, User


def test_load_data():

    os.makedirs("data", exist_ok=True)

    # Initialize database and create users table
    Base.metadata.drop_all(bind=engine)  # Clean slate
    Base.metadata.create_all(bind=engine)  # Create tables

    df = pd.DataFrame({
        "id": [1],  # Add missing 'id' column
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"]
    })

    df.to_csv("data/users.csv", index=False)

    load_data()

    # Query PostgreSQL instead of SQLite
    db = SessionLocal()
    result = db.query(User).all()
    db.close()

    assert len(result) == 1
    assert result[0].name == "Testuser"