from unittest.mock import patch, MagicMock
import pandas as pd
from load.load_data import load_data


@patch("load.load_data.engine")
def test_load_data(mock_engine):
    # Create sample DataFrame
    sample_df = pd.DataFrame({
        "id": [1],
        "name": ["Alice"],
        "username": ["alice123"],
        "email": ["alice@example.com"]
    })

    # Mock DataFrame.to_sql
    sample_df.to_sql = MagicMock()

    # Call function
    load_data(sample_df)

    # Verify to_sql was called correctly
    sample_df.to_sql.assert_called_once_with(
        "users",
        mock_engine,
        if_exists="replace",
        index=False
    )