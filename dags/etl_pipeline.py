from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from extract.extract_api import extract_data
from transform.transform_data import transform_data
from load.load_data import load_data

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 7, 13),
}

with DAG(
    dag_id="enterprise_etl_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    extract_task >> transform_task >> load_task