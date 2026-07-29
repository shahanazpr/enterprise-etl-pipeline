import json
import os
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()

BASE_DIR = "/opt/airflow/project"


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
def extract_data():

    url = os.getenv("API_URL")

    json_path = os.path.join(BASE_DIR, "data", "users.json")

    try:
        logger.info("Connecting to API...")

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