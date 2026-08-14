import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed

from utils.logger import logger, log_execution_time


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True,
)
@log_execution_time
def upload_to_s3(file_path, bucket_name, object_name=None):
    """
    Upload a file to an AWS S3 bucket with retry support.
    """
    if not bucket_name:
        logger.warning("S3 bucket not configured. Skipping S3 upload.")
        return False

    if object_name is None:
        current_date = datetime.now().strftime("%Y-%m-%d")
        object_name = f"raw_data/{current_date}/{file_path.split('/')[-1]}"

    try:
        s3_client = boto3.client("s3")

        s3_client.upload_file(
            file_path,
            bucket_name,
            object_name,
        )

        logger.info(
            f"Successfully uploaded '{file_path}' "
            f"to bucket '{bucket_name}' as '{object_name}'."
        )

        return True

    except ClientError as e:
        logger.error(f"S3 upload failed: {e}")
        raise