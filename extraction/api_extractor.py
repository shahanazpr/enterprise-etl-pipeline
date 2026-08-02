import requests
import json
import os

from tenacity import retry, stop_after_attempt, wait_fixed
from config.logger import logger


# Retry the API call up to 3 times with a 2-second wait
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_users():

    url = "https://jsonplaceholder.typicode.com/users"

    logger.info("Fetching data from API...")

    response = requests.get(url)

    logger.info(f"Status Code: {response.status_code}")

    response.raise_for_status()

    return response.json()


def save_data(data):

    os.makedirs("raw_data", exist_ok=True)

    with open("raw_data/users.json", "w") as file:
        json.dump(data, file, indent=4)


def main():

    try:

        users = fetch_users()

        save_data(users)

        logger.info(f"{len(users)} records saved successfully.")

        print("✅ ETL Extraction Completed!")

    except Exception as e:

        logger.exception(e)

        print("❌ Extraction Failed")


if __name__ == "__main__":
    main()