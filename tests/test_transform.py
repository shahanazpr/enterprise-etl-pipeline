import os
import pandas as pd
from pathlib import Path
from transform.transform_data import transform_data


def test_transform_data():
    root_dir = Path(__file__).parent.parent
    data_dir = root_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    json_file = data_dir / "users.json"

    # Create a DataFrame with columns matching what transform_data expects
    df = pd.DataFrame({
        "id": [1, 2],
        "name": [" Testuser ", "Testuser "],
        "username": [" user1 ", "user1 "],
        "email": ["TEST@MAIL.COM", "TEST@MAIL.COM"],
        "phone": ["123-456", "789-012"],
        "website": ["test1.com", "test2.com"]
    })

    # Save as standard table-oriented JSON so pandas reads columns correctly
    df.to_json(json_file, orient="table", index=False)

    transform_data()

    output_csv = data_dir / "users.csv"
    output = pd.read_csv(output_csv)

    assert len(output) == 2
    assert output.loc[0, "name"] == "Testuser"
    assert output.loc[0, "email"] == "test@mail.com"