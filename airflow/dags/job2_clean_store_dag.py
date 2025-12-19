from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="job2_clean_store",
    start_date=datetime(2024, 12, 1),
    schedule="@hourly",
    catchup=False
)as dag:
    BashOperator(
        task_id="clean_store",
        bash_command="python src/job2_cleaner.py"
    )