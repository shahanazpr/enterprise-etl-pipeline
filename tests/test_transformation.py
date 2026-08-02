import pandas as pd


def test_dataframe_columns():
    df = pd.read_csv("raw_data/cleaned_users.csv")

    expected_columns = [
        "id",
        "name",
        "username",
        "email",
        "phone",
        "website",
        "city",
        "zipcode",
        "company_name"
    ]

    assert list(df.columns) == expected_columns