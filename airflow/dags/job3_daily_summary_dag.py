from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="job3_daily_summary",
    start_date=datetime(2024, 12, 1),
    schedule="@daily",
    catchup=False
)as dag:
    BashOperator(
        task_id="daily_analytics",
        bash_command="python src/job3_analytics.py"
    )