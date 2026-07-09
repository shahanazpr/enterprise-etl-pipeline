import json
import os
import requests

from dotenv import load_dotenv
from utils.logger import logger
from models.user_model import User

load_dotenv()


def extract_data():

    url = os.getenv("API_URL")

    try:
        logger.info("Connecting to API...")

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        # Validate API data using Pydantic
        validated_data = []

        for user in data:
            validated_user = User(**user)
            validated_data.append(validated_user.model_dump())

        with open("data/users.json", "w") as file:
            json.dump(validated_data, file, indent=4)

        logger.info("Data extracted and validated successfully.")

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")

    except Exception as e:
        logger.error(f"Validation Error: {e}")