from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys

default_args = {
    "owner": "rxtrack",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_etl():
    subprocess.run(
        [sys.executable, "/mnt/c/Users/bnkol/Downloads/rxtrack/etl/etl_pipeline.py"],
        check=True
    )

with DAG(
    dag_id="rxtrack_etl_pipeline",
    default_args=default_args,
    description="Daily ETL pipeline for RxTrack pharmacy inventory",
    schedule_interval="0 0 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    run_etl_task = PythonOperator(
        task_id="run_etl_pipeline",
        python_callable=run_etl,
    )