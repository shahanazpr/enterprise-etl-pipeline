from extract.extract_api import extract_data
from transform.transform_data import transform_data
from load.load_data import load_data


def main():
    print("\n===== Enterprise ETL Pipeline =====")

    extract_data()
    transform_data()
    load_data()

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()