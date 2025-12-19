# airflow/dags/job1_ingestion_dag.py

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="job1_ingestion",
    start_date=datetime(2024, 12, 1),
    schedule=None,          
    catchup=False,
    tags=["ingestion", "kafka"]
) as dag:

    BashOperator(
        task_id="run_producer",
        bash_command="python src/job1_producer.py"
    )
