import pandas as pd
from unittest.mock import patch
from transform.transform_data import transform_data


@patch("transform.transform_data.pd.DataFrame.to_csv")
@patch("transform.transform_data.pd.read_json")
def test_transform_data(mock_read_json, mock_to_csv):
    # Sample input DataFrame
    sample_df = pd.DataFrame({
        "name": [" alice ", "BOB "],
        "username": [" alice123 ", " bob456 "],
        "email": [" ALICE@MAIL.COM ", " BOB@MAIL.COM "]
    })

    mock_read_json.return_value = sample_df

    # Run the transformation
    transform_data()

    # Verify read_json was called
    mock_read_json.assert_called_once_with("data/users.json")

    # Verify transformations
    assert sample_df["name"].tolist() == ["Alice", "Bob"]
    assert sample_df["username"].tolist() == ["alice123", "bob456"]
    assert sample_df["email"].tolist() == ["alice@mail.com", "bob@mail.com"]

    # Verify CSV was written
    mock_to_csv.assert_called_once_with("data/users.csv", index=False)