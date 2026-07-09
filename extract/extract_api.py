import json
import requests
from utils.logger import logger


def extract_data():
    url = "https://jsonplaceholder.typicode.com/users"

    try:
        logger.info("Connecting to API...")

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        with open("data/users.json", "w") as file:
            json.dump(data, file, indent=4)

        logger.info("Data extracted successfully.")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")