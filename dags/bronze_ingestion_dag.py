from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

INPUT_PATH = "/opt/airflow/data/dataset.parquet"
OUTPUT_FILE = "/opt/airflow/data/bronze/taxi_bronze.parquet"

with DAG(
    dag_id="bronze_ingestion",
    description="Ingest raw taxi data into Bronze layer",
    start_date=datetime(2026, 1, 16),
    schedule="@daily",
    catchup=False,
    tags=["bronze", "etl"],
) as dag:

    ingest_bronze = BashOperator(
        task_id="load_raw_data_to_bronze",
        bash_command=(
            "spark-submit /opt/airflow/spark_jobs/bronze_ingestion.py "
            "--input /opt/airflow/data/dataset.parquet "
            "--output /opt/airflow/data/bronze/taxi_bronze.parquet"
        ),
    )

    # ingest_bronze
