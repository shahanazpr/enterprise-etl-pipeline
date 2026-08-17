import json
import os
import requests
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_fixed

from config import settings
from utils.logger import logger, log_execution_time
from utils.s3_upload import upload_to_s3
from validation.user_model import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Records requested per page. Kept generous by default so a real run against
# an endpoint like JSONPlaceholder's /users (10 total records) still completes
# in a single page — set API_PAGE_LIMIT lower (e.g. 3) to force multi-page
# behavior for testing/demo purposes.
DEFAULT_PAGE_LIMIT = int(os.getenv("API_PAGE_LIMIT", "100"))
MAX_PAGES = int(os.getenv("API_MAX_PAGES", "50"))  # safety cap against infinite loops


def fetch_all_pages(url, page_limit=DEFAULT_PAGE_LIMIT, max_pages=MAX_PAGES):
    """
    Fetch every record from a paginated REST API endpoint.

    Uses the _page / _limit query-parameter convention (supported by
    JSONPlaceholder and many similar REST APIs). Keeps requesting the next
    page until a page comes back empty or with fewer records than the
    requested limit, which signals the last page has been reached.

    Two safety guards are built in, since not every API actually honors
    _page/_limit (some silently ignore unknown query params and just
    return the full dataset every time):
      - If a page returns the exact same set of record IDs as the
        previous page, pagination is assumed to be unsupported by this
        endpoint and the loop stops after that page.
      - A hard cap (max_pages) prevents an unbounded loop in any other
        unexpected case.

    Rate-limit responses (HTTP 429) are logged explicitly with any
    Retry-After header the API provides, then re-raised so the existing
    @retry decorator on extract_data() can retry the whole extraction
    with a backoff delay.
    """
    all_records = []
    previous_page_ids = None
    page = 1

    while page <= max_pages:
        logger.info(f"Fetching page {page} (limit={page_limit})...")

        response = requests.get(
            url,
            params={"_page": page, "_limit": page_limit},
            timeout=10,
        )

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "unknown")
            logger.warning(
                f"Rate limited by API (HTTP 429) on page {page}. "
                f"Retry-After: {retry_after}s. Will retry via extract_data() retry policy."
            )

        response.raise_for_status()
        page_data = response.json()

        if not page_data:
            logger.info(f"Page {page} returned no records \u2014 pagination complete.")
            break

        current_page_ids = {record.get("id") for record in page_data}
        if current_page_ids == previous_page_ids:
            logger.warning(
                f"Page {page} returned identical records to the previous page \u2014 "
                "this endpoint likely does not support _page/_limit pagination. "
                "Stopping to avoid duplicate data."
            )
            break

        all_records.extend(page_data)
        logger.info(
            f"Page {page} returned {len(page_data)} records "
            f"(running total: {len(all_records)})."
        )

        if len(page_data) < page_limit:
            logger.info("Received a partial page \u2014 this was the last page.")
            break

        previous_page_ids = current_page_ids
        page += 1
    else:
        logger.warning(f"Reached the max_pages safety limit ({max_pages}). Stopping.")

    return all_records


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True,
)
@log_execution_time
def extract_data():

    url = settings.API_URL

    # Ensure the data directory exists dynamically before writing to it
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    json_path = os.path.join(BASE_DIR, "data", "users.json")

    try:
        logger.info(f"Connecting to API: {url}")

        data = fetch_all_pages(url)

        logger.info(f"Successfully fetched {len(data)} records across all pages.")

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
                    f"Validation failed for record ID {record.get('id', 'Unknown')}: {e}"
                )

        # Save only valid records
        with open(json_path, "w") as file:
            json.dump(valid_data, file, indent=4)

        logger.info(f"Valid records: {len(valid_data)}")
        if skipped_records > 0:
            logger.warning(f"Skipped {skipped_records} invalid records.")
        logger.info(f"JSON saved at: {json_path}")

        # Upload JSON file to AWS S3
        upload_to_s3(
            file_path=json_path,
            bucket_name=settings.S3_BUCKET_NAME,
        )

    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise
