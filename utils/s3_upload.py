import boto3
from botocore.exceptions import ClientError

from utils.logger import logger, log_execution_time


@log_execution_time
def upload_to_s3(file_path, bucket_name, object_name=None):
    """
    Upload a file to an AWS S3 bucket.
    """

    if object_name is None:
        object_name = file_path

    try:
        s3_client = boto3.client("s3")
        s3_client.upload_file(file_path, bucket_name, object_name)

        logger.info(
            f"Successfully uploaded '{file_path}' to bucket '{bucket_name}' as '{object_name}'."
        )
        return True

    except ClientError as e:
        logger.error(f"S3 upload failed: {e}")
        return False