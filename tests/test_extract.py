from unittest.mock import patch, mock_open
from extract.extract_api import extract_data


@patch("extract.extract_api.json.dump")
@patch("extract.extract_api.open", new_callable=mock_open)
@patch("extract.extract_api.requests.get")
def test_extract_data(mock_get, mock_file, mock_json_dump):
    # Mock API response
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Alice",
            "username": "alice123",
            "email": "alice@example.com"
        }
    ]

    # Execute extraction
    extract_data()

    # Verify API request
    mock_get.assert_called_once()

    # Verify file creation
    mock_file.assert_called_once_with("data/users.json", "w")

    # Verify JSON write
    mock_json_dump.assert_called_once()