from extract.extract_api import extract_data
from transform.transform_data import transform_data
from load.load_data import load_data
from utils.logger import logger
from notifications.notifier import send_email_alert
import os


def main():
    print("\n===== Enterprise ETL Pipeline =====")

    logger.info("ETL Pipeline Started")

    try:
        extract_data()
        transform_data()
        load_data()

        logger.info("ETL Pipeline Completed Successfully")
        print("Pipeline completed successfully!")

    except Exception as e:
        logger.exception(f"ETL Pipeline Failed: {e}")

        send_email_alert(
            sender=os.getenv("EMAIL_SENDER"),
            password=os.getenv("EMAIL_PASSWORD"),
            receiver=os.getenv("EMAIL_RECEIVER"),
            subject="ETL Pipeline Failed",
            body=str(e)
        )

        print("Pipeline failed!")


if __name__ == "__main__":
    main()