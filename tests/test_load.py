import os
import pandas as pd
from load.load_data import load_data
from database import SessionLocal
from models.user import User


def test_load_data():
    # Ensure directory exists matching production code expectation
    os.makedirs("data", exist_ok=True)

    # DataFrame with all required columns
    df = pd.DataFrame({
        "id": [1],
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"],
        "phone": ["123-456-7890"],
        "website": ["test.com"]
    })

    # Save using the exact relative path string
    df.to_csv("data/users.csv", index=False)

    # Run the load function
    load_data()

    # Query the database
    db = SessionLocal()
    try:
        users = db.query(User).all()
        assert len(users) >= 1
        names = [u.name for u in users]
        assert "Testuser" in names
    finally:
        db.close()