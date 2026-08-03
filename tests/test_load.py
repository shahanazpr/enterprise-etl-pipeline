import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from load.load_data import load_data


@patch("load.load_data.SessionLocal")
def test_load_data(mock_session):

    # Mock database session
    db = MagicMock()
    mock_session.return_value = db

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

    # Verify database operations
    db.query.assert_called_once()
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.close.assert_called_once()


@patch("load.load_data.SessionLocal")
@patch("load.load_data.pd.read_csv")
def test_load_data_csv_error(mock_read_csv, mock_session):

    db = MagicMock()
    mock_session.return_value = db

    mock_read_csv.side_effect = Exception("CSV file error")

    with pytest.raises(Exception, match="CSV file error"):
        load_data()

    db.rollback.assert_called_once()
    db.close.assert_called_once()