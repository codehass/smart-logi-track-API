import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


DB_USER = os.getenv("DATABASE_USER", "airflow")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "123456")
DB_NAME = os.getenv("DATABASE_NAME", "smart_logi_track_db")
DB_HOST = os.getenv("DATABASE_HOST", "postgres")


JDBC_URL = f"jdbc:postgresql://{DB_HOST}:5432/{DB_NAME}"

# MODEL_OUTPUT = "/opt/airflow/models/gbt_model"
SILVER_DB_TABLE = "public.silver_data"
SCRIPT_PATH = "/opt/airflow/spark_jobs/ml_training.py"
JDBC_JAR = "/opt/airflow/postgresql-42.6.0.jar"

with DAG(
    dag_id="ml_training",
    start_date=datetime(2026, 1, 20),
    schedule=None,
    catchup=False,
    tags=["ml", "training"],
) as dag:

    train_model = BashOperator(
        task_id="run_ml_training",
        bash_command=(
            f"mkdir -p /opt/airflow/models && "
            f"spark-submit --jars {JDBC_JAR} {SCRIPT_PATH} "
            f"--jdbc-url '{JDBC_URL}' "
            f"--db-table {SILVER_DB_TABLE} "
            f"--db-user {DB_USER} "
            f"--db-password {DB_PASSWORD} "
            # f"--model-output {MODEL_OUTPUT}"
        ),
    )

    train_model
