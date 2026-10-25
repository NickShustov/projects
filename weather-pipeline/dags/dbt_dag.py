from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

DBT_DIR = "/usr/local/airflow/dags/dbt/my_dbt"
DBT_BIN = "/usr/local/airflow/dbt_venv312/bin/dbt"
ENV = "DBT_LOG_PATH=/tmp/dbt_logs DBT_TARGET_PATH=/tmp/dbt_target"

with DAG(
    dag_id="dbt_daily",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && {ENV} {DBT_BIN} run --profiles-dir .",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {ENV} {DBT_BIN} test --profiles-dir .",
    )
    dbt_run >> dbt_test
