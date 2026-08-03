from extract.extract_api import extract_data
from transform.transform_data import transform_data
from load.load_data import load_data
from utils.logger import logger


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
        load_data(df)
        logger.info("Data loading completed.")

        print("Pipeline completed successfully!")
        logger.info("===== ETL Pipeline Finished Successfully =====")

    except Exception as e:
        logger.error(f"ETL Pipeline Failed: {e}")
        raise


if __name__ == "__main__":
    main()