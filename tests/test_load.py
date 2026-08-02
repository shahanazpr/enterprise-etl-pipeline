import os
import pandas as pd

from load.load_data import load_data
from database import SessionLocal
from models.user import User


def test_load_data():

    os.makedirs("data", exist_ok=True)

    # Make sure your test DataFrame includes ALL required columns that your load_data expects!
    df = pd.DataFrame({
        "id": [1],
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"],
        "phone": ["123-456-7890"],
        "website": ["test.com"]
    })

    df.to_csv("data/users.csv", index=False)

    # Run the load function (this inserts into PostgreSQL)
    load_data()

    # Query the PostgreSQL database using SQLAlchemy session
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        assert len(users) == 1
        assert users[0].name == "Testuser"
    finally:
        db.close()