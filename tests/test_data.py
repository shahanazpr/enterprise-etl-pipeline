from unittest.mock import patch
from extract.extract_api import extract_data

@patch("extract.extract_api.requests.get")
def test_extract_data(mock_get):
    # Arrange: Mock the API response to return exactly 1 user
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com"
        }
    ]

    # Act: Call the extract function
    data = extract_data()

    # Assert: Verify that it extracted exactly 1 user successfully
    assert len(data) == 1
    assert data[0]["name"] == "Test User"