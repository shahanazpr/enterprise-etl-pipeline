import json
import os
import requests

from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()


def extract_data():

    url = os.getenv("API_URL")

    try:
        logger.info("Connecting to API...")

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        with open("data/users.json", "w") as file:
            json.dump(data, file, indent=4)

        logger.info("Data extracted successfully.")

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")