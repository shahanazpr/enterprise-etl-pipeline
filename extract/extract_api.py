import json
import os
import requests
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_fixed

from config import settings
from utils.logger import logger
from validation.user_model import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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

        logger.info(f"Successfully fetched {len(data)} records.")

        valid_data = []
        skipped_records = 0

        for record in data:
            try:
                # Map API response to User model
                user = {
                    "id": record.get("id"),
                    "name": record.get("name"),
                    "username": record.get("username"),
                    "email": record.get("email"),
                    "phone": record.get("phone"),
                    "website": record.get("website"),
                    "city": record.get("address", {}).get("city"),
                    "zipcode": record.get("address", {}).get("zipcode"),
                    "company_name": record.get("company", {}).get("name"),
                }

                # Validate record using Pydantic
                User(**user)

                # Keep original record for transformation
                valid_data.append(record)

            except ValidationError as e:
                skipped_records += 1
                logger.error(
                    f"Skipping invalid record ID {record.get('id', 'Unknown')}: {e}"
                )

        # Save only valid records
        with open(json_path, "w") as file:
            json.dump(valid_data, file, indent=4)

        logger.info(f"Valid records: {len(valid_data)}")
        logger.info(f"Skipped records: {skipped_records}")
        logger.info(f"JSON saved at: {json_path}")

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise