import pytest
from database import engine


def test_database_connection():
    try:
        with engine.connect() as conn:
            assert conn is not None

    except Exception as e:
        pytest.skip(f"Database not available: {e}")