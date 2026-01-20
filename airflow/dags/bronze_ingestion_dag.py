from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

with DAG(
    dag_id="bronze_ingestion",
    start_date=datetime(2026, 1, 20),
    schedule="@daily",
    catchup=False,
    tags=["bronze", "etl"],
) as dag:

    ingest_bronze = BashOperator(
        task_id="load_raw_data_to_bronze",
        bash_command=(
            "mkdir -p /opt/airflow/data/bronze && "
            "spark-submit /opt/airflow/spark_jobs/bronze_ingestion.py "
            "--input /opt/airflow/data/dataset.parquet "
            "--output /opt/airflow/data/bronze/taxi_bronze.parquet"
        ),
    )

    trigger_silver = TriggerDagRunOperator(
        task_id="trigger_silver",
        trigger_dag_id="silver_processing",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    ingest_bronze >> trigger_silver
