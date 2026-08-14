from dotenv import load_dotenv
import os

load_dotenv()

# API Key
API_URL = os.getenv("API_URL")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

# AWS S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

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