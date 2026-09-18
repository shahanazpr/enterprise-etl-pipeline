import pandas as pd
from unittest.mock import patch, MagicMock

from load.load_data import load_data


@patch("load.load_data.SessionLocal")
def test_load_data(mock_session):
    db = MagicMock()
    mock_session.return_value = db

    # Make the database report that the user does not already exist.
    db.query.return_value.filter.return_value.first.return_value = None

    df = pd.DataFrame({
        "id": [1],
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"],
        "phone": ["123-456-7890"],
        "website": ["test.com"]
    })

    load_data(df)

    db.query.assert_called_once()
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.close.assert_called_once()


@patch("load.load_data.SessionLocal")
def test_load_data_empty_dataframe(mock_session):
    db = MagicMock()
    mock_session.return_value = db

    df = pd.DataFrame()

    load_data(df)

    db.commit.assert_not_called()
    db.close.assert_called_once()


@patch("load.load_data.SessionLocal")
def test_load_data_none(mock_session):
    db = MagicMock()
    mock_session.return_value = db

    load_data(None)

    db.commit.assert_not_called()
    db.close.assert_called_once()


@patch("load.load_data.SessionLocal")
def test_load_data_database_error(mock_session):
    db = MagicMock()
    mock_session.return_value = db

    db.query.side_effect = Exception("Database error")

    df = pd.DataFrame({
        "id": [1],
        "name": ["Testuser"],
        "username": ["user1"],
        "email": ["abc@gmail.com"],
        "phone": ["123-456-7890"],
        "website": ["test.com"]
    })

    load_data(df)

    # Database errors inside a row are skipped by the loader.
    db.rollback.assert_not_called()
    db.close.assert_called_once()