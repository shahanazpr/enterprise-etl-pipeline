import json
import os
from pathlib import Path
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from config import settings
from utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True,
)
def extract_data():

    url = settings.API_URL

    # Ensure the data directory exists dynamically before writing to it
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    json_path = os.path.join(BASE_DIR, "data", "users.json")

    try:
        logger.info(f"Connecting to API: {url}")

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)

        logger.info(f"Successfully extracted {len(data)} records.")
        logger.info(f"JSON saved at: {json_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        raise

    except Exception as e:
        logger.error(f"Extraction Error: {e}")
        raise