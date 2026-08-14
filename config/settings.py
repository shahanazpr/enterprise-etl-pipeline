from dotenv import load_dotenv
import os

load_dotenv()

# API Key
API_URL = os.getenv("API_URL")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if __name__ == "__main__":
    print("Database:", DB_NAME)
    print("Host:", DB_HOST)
    print("User:", DB_USER)