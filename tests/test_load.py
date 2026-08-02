import sqlite3
import os
import pandas as pd

from load.load_data import load_data


def test_load_data():

    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame({
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"]
    })

    df.to_csv("data/users.csv", index=False)

    load_data()

    conn = sqlite3.connect("data/users.db")

    result = pd.read_sql("SELECT * FROM users", conn)

    conn.close()

    assert len(result) == 1
    assert result.iloc[0]["name"] == "Testuser"