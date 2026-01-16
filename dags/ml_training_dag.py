from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

MODEL_OUTPUT = "/opt/airflow/models/gbt_model"
SILVER_DB_TABLE = "silver_data"
JDBC_URL = "jdbc:postgresql://postgres:5432/airflow"
DB_USER = "airflow"
DB_PASSWORD = "airflow"
SCRIPT_PATH = "/opt/airflow/spark_jobs/ml_training.py"
JDBC_JAR = "/opt/airflow/postgresql-42.6.0.jar"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ml_training",
    description="Train ML model on Silver data",
    start_date=datetime(2026, 1, 16),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["ml", "training"],
) as dag:

    wait_for_silver = ExternalTaskSensor(
        task_id="wait_for_silver",
        external_dag_id="silver_processing",
        external_task_id="clean_bronze_to_silver",
        mode="poke",
        poke_interval=60,
        timeout=3600,
    )

    train_model = BashOperator(
        task_id="run_ml_training",
        bash_command=(
            f"spark-submit --jars {JDBC_JAR} {SCRIPT_PATH} "
            f"--jdbc-url {JDBC_URL} "
            f"--db-table {SILVER_DB_TABLE} "
            f"--db-user {DB_USER} "
            f"--db-password {DB_PASSWORD} "
            f"--model-output {MODEL_OUTPUT}"
        ),
    )

    wait_for_silver >> train_model
