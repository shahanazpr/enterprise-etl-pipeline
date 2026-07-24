import os
import pandas as pd
from transform.transform_data import transform_data


def test_transform_data():

    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame({
        "name": [" Testuser ", "Testuser "],
        "username": [" user1 ", "user1 "],
        "email": ["TEST@MAIL.COM", "TEST@MAIL.COM"]
    })

    df.to_json("data/users.json")

    transform_data()

    output = pd.read_csv("data/users.csv")

    assert len(output) == 2
    assert output.loc[0, "name"] == "Testuser"
    assert output.loc[0, "email"] == "test@mail.com"
    assert output.loc[1, "name"] == "Testuser"
    assert output.loc[1, "email"] == "test@mail.com"