from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


# Function to print the current date and time
def print_time():
    print(f"Current time is: {datetime.now()}")


def print_time1():
    print("Hello from task one")


# Define the default_args dictionary
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 15),
    "retries": 1,
}

# Instantiate the DAG
dag = DAG(
    "simple_print_time_dag",  # DAG name
    default_args=default_args,
    description="A simple DAG that prints current time",
    schedule_interval="@daily",  # Run daily
)

# Define the task using PythonOperator
print_time_task1 = PythonOperator(
    task_id="print_time1",  # Task ID
    python_callable=print_time1,  # Python function to call
    dag=dag,
)

print_time_task2 = PythonOperator(
    task_id="print_time2",  # Task ID
    python_callable=print_time,  # Python function to call
    dag=dag,
)

# Set the task
print_time_task1 >> print_time_task2
