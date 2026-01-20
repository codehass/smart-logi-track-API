from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

BRONZE_PATH = "/opt/airflow/data/bronze/taxi_bronze.parquet"
SPARK_JOB = "/opt/airflow/spark_jobs/silver_processing.py"
JDBC_DRIVER = "/opt/airflow/postgresql-42.6.0.jar"

with DAG(
    dag_id="silver_processing",
    start_date=datetime(2026, 1, 20),
    schedule=None,
    catchup=False,
    tags=["silver", "etl"],
) as dag:

    clean_and_save_silver = BashOperator(
        task_id="clean_bronze_to_silver",
        bash_command=f"spark-submit --jars {JDBC_DRIVER} {SPARK_JOB} --input {BRONZE_PATH}",
    )

    trigger_ml = TriggerDagRunOperator(
        task_id="trigger_ml",
        trigger_dag_id="ml_training",
        reset_dag_run=True,
        wait_for_completion=False,
    )

    clean_and_save_silver >> trigger_ml
