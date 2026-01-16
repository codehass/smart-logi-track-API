from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

BRONZE_PATH = "/opt/airflow/data/bronze/taxi_bronze.parquet"
SPARK_JOB = "/opt/airflow/spark_jobs/silver_processing.py"
JDBC_DRIVER = "/opt/airflow/postgresql-42.6.0.jar"

with DAG(
    dag_id="silver_processing",
    description="Clean Bronze data and save Silver data to Postgres",
    start_date=datetime(2026, 1, 16),
    schedule="@daily",
    catchup=False,
    tags=["silver", "etl"],
) as dag:

    clean_and_save_silver = BashOperator(
        task_id="clean_bronze_to_silver",
        bash_command=(
            f"spark-submit --jars {JDBC_DRIVER} "
            f"{SPARK_JOB} "
            f"--input {BRONZE_PATH}"
        ),
    )

    clean_and_save_silver
