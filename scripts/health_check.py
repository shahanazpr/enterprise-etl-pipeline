import os
import requests
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Read environment variables
API_URL = os.getenv("API_URL")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def check_api():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            print("✓ API connection successful")
        else:
            print(f"✗ API returned status code {response.status_code}")
    except Exception as e:
        print(f"✗ API check failed: {e}")


def check_database():
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")


def check_csv():
    if os.path.exists("data/users.csv"):
        print("✓ users.csv found")
    else:
        print("✗ users.csv not found")


if __name__ == "__main__":
    print("=== ETL Health Check ===")
    check_api()
    check_database()
    check_csv()