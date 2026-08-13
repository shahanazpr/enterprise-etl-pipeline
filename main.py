from extract.extract_api import extract_data
from transform.transform_data import transform_data
from loading.upsert_users import upsert_users
from utils.logger import logger, log_execution_time
from notifications.notifier import send_email_alert
import os


@log_execution_time
def main():
    print("\n===== Enterprise ETL Pipeline =====")

    logger.info("===== ETL Pipeline Started =====")

    try:
        logger.info("Starting data extraction...")
        extract_data()
        logger.info("Data extraction completed.")

        logger.info("Starting data transformation...")
        df = transform_data()
        logger.info("Data transformation completed.")

        logger.info("Starting data loading...")
        upsert_users()
        logger.info("Data loading completed.")

        logger.info("===== ETL Pipeline Completed Successfully =====")
        print("Pipeline completed successfully!")

    except Exception as e:
        logger.exception(f"ETL Pipeline Failed: {e}")

        send_email_alert(
            sender=os.getenv("SMTP_SENDER"),
            password=os.getenv("SMTP_PASSWORD"),
            receiver=os.getenv("EMAIL_RECEIVER"),
            subject="ETL Pipeline Failed",
            body=str(e)
        )

        print("Pipeline failed!")
        raise


if __name__ == "__main__":
    main()