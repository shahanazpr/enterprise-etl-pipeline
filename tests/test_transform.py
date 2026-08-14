import os
import pandas as pd
import pytest
from unittest.mock import patch

from transform.transform_data import transform_data, BASE_DIR


@patch("transform.transform_data.pd.DataFrame.to_csv")
@patch("transform.transform_data.pd.read_json")
def test_transform_data(mock_read_json, mock_to_csv):

    sample_df = pd.DataFrame({
        "id": [1, 2],
        "name": [" alice ", "BOB "],
        "username": [" alice123 ", " bob456 "],
        "email": [" ALICE@MAIL.COM ", " BOB@MAIL.COM "],
        "phone": ["123-456", "789-012"],
        "website": ["alice.com", "bob.com"]
    })

    mock_read_json.return_value = sample_df

    transform_data()

    input_file = os.path.join(BASE_DIR, "data", "users.json")

    mock_read_json.assert_called_once_with(
        input_file,
        
    )

    assert sample_df["name"].tolist() == ["Alice", "Bob"]
    assert sample_df["username"].tolist() == ["alice123", "bob456"]
    assert sample_df["email"].tolist() == ["alice@mail.com", "bob@mail.com"]

    output_file = os.path.join(BASE_DIR, "data", "users.csv")

    mock_to_csv.assert_called_once_with(
        output_file,
        index=False
    )


@patch("transform.transform_data.pd.read_json")
def test_transform_data_read_json_error(mock_read_json):

    mock_read_json.side_effect = Exception("Failed to read JSON")

    with pytest.raises(Exception, match="Failed to read JSON"):
        transform_data()