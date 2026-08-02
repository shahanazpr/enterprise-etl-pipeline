import os
import pandas as pd
from pathlib import Path
from load.load_data import load_data
from database import SessionLocal
from models.user import User


def test_load_data():
    # Ensure the data directory exists globally relative to the workspace root
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Define the exact file path
    csv_file = data_dir / "users.csv"

    # Make sure your test DataFrame includes ALL required columns
    df = pd.DataFrame({
        "id": [1],
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"],
        "phone": ["123-456-7890"],
        "website": ["test.com"]
    })

    # Save CSV using the explicit path
    df.to_csv(csv_file, index=False)

    # Run the load function (this inserts into PostgreSQL)
    load_data()

    # Query the PostgreSQL database using SQLAlchemy session
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        assert len(users) >= 1
        # Check if our test user exists in the database
        names = [u.name for u in users]
        assert "Testuser" in names
    finally:
        db.close()