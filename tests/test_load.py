import os
from pathlib import Path
import pandas as pd
from load.load_data import load_data
from database import SessionLocal
from models.user import User


def test_load_data():
    root_dir = Path(__file__).parent.parent
    data_dir = root_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_file = data_dir / "users.csv"

    df = pd.DataFrame({
        "id": [1],
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"],
        "phone": ["123-456-7890"],
        "website": ["test.com"]
    })

    df.to_csv(csv_file, index=False)

    load_data()

    db = SessionLocal()
    try:
        users = db.query(User).all()
        assert len(users) >= 1
        names = [u.name for u in users]
        assert "Testuser" in names
    finally:
        db.close()