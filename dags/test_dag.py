from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

# =========================
# Common paths & configs
# =========================

DATASET_PATH = "/opt/airflow/data/dataset.parquet"
BRONZE_PATH = "/opt/airflow/data/bronze/taxi_bronze.parquet"

SILVER_SPARK_JOB = "/opt/airflow/spark_jobs/silver_processing.py"
BRONZE_SPARK_JOB = "/opt/airflow/spark_jobs/bronze_ingestion.py"
ML_SPARK_JOB = "/opt/airflow/spark_jobs/ml_training.py"

JDBC_JAR = "/opt/airflow/postgresql-42.6.0.jar"
JDBC_URL = "jdbc:postgresql://postgres:5432/airflow"
DB_USER = "airflow"
DB_PASSWORD = "airflow"
SILVER_TABLE = "silver_data"
MODEL_OUTPUT = "/opt/airflow/models/gbt_model"

START_DATE = datetime(2026, 1, 16)

# =====================================================
# DAG 1 — Bronze ingestion
# =====================================================

with DAG(
    dag_id="bronze_ingestion",
    description="Ingest raw data into Bronze layer",
    start_date=START_DATE,
    schedule="@daily",
    catchup=False,
    tags=["bronze", "etl"],
) as bronze_dag:

    load_raw_data_to_bronze = BashOperator(
        task_id="load_raw_data_to_bronze",
        bash_command=(
            f"spark-submit {BRONZE_SPARK_JOB} "
            f"--input {DATASET_PATH} "
            f"--output {BRONZE_PATH}"
        ),
    )


# =====================================================
# DAG 2 — Silver processing
# =====================================================

with DAG(
    dag_id="silver_processing",
    description="Transform Bronze data into Silver",
    start_date=START_DATE,
    schedule="@daily",
    catchup=False,
    tags=["silver", "etl"],
) as silver_dag:

    wait_for_bronze = ExternalTaskSensor(
        task_id="wait_for_bronze",
        external_dag_id="bronze_ingestion",
        external_task_id="load_raw_data_to_bronze",
        mode="poke",
        poke_interval=60,
        timeout=3600,
    )

    clean_bronze_to_silver = BashOperator(
        task_id="clean_bronze_to_silver",
        bash_command=(
            f"spark-submit --jars {JDBC_JAR} "
            f"{SILVER_SPARK_JOB} "
            f"--input {BRONZE_PATH}"
        ),
    )

    wait_for_bronze >> clean_bronze_to_silver


# =====================================================
# DAG 3 — ML training
# =====================================================

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ml_training",
    description="Train ML model on Silver data",
    start_date=START_DATE,
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["ml", "training"],
) as ml_dag:

    wait_for_silver = ExternalTaskSensor(
        task_id="wait_for_silver",
        external_dag_id="silver_processing",
        external_task_id="clean_bronze_to_silver",
        mode="poke",
        poke_interval=60,
        timeout=3600,
    )

    run_ml_training = BashOperator(
        task_id="run_ml_training",
        bash_command=(
            f"spark-submit --jars {JDBC_JAR} {ML_SPARK_JOB} "
            f"--jdbc-url {JDBC_URL} "
            f"--db-table {SILVER_TABLE} "
            f"--db-user {DB_USER} "
            f"--db-password {DB_PASSWORD} "
            f"--model-output {MODEL_OUTPUT}"
        ),
    )

    wait_for_silver >> run_ml_training
