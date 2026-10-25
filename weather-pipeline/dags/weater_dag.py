import pendulum
import requests
from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

LAT, LON = 55.75, 37.62 

DBT_DIR = "/usr/local/airflow/dags/dbt/my_dbt"
DBT_BIN = "/usr/local/airflow/dbt_venv312/bin/dbt"
ENV = "DBT_LOG_PATH=/tmp/dbt_logs DBT_TARGET_PATH=/tmp/dbt_target"

with DAG(
    dag_id="weather_load",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2},
    tags=["weather", "dbt"],
) as dag:

    @task
    def extract():
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": LAT,
                "longitude": LON,
                "daily": "temperature_2m_mean,wind_speed_10m_max,surface_pressure_mean",
                "past_days": 7,
                "forecast_days": 1,
                "timezone": "auto",
            },
            timeout=30,
        )
        r.raise_for_status()
        d = r.json()["daily"]
        return list(zip(
            d["time"],
            d["temperature_2m_mean"],
            d["wind_speed_10m_max"],
            d["surface_pressure_mean"],
        ))

    @task
    def load(rows):
        hook = PostgresHook(postgres_conn_id="dwh")
        hook.run("""
            CREATE TABLE IF NOT EXISTS raw.weather (
                weather_date DATE PRIMARY KEY,
                temperature NUMERIC(5,2),
                wind_speed NUMERIC(5,2),
                pressure NUMERIC(7,2),
                loaded_at TIMESTAMP DEFAULT now()
            )
        """)
        hook.insert_rows(
            table="raw.weather",
            rows=rows,
            target_fields=["weather_date", "temperature", "wind_speed", "pressure"],
            replace=True,
            replace_index="weather_date",
        )
        print(f"Загружено строк: {len(rows)}")

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && {ENV} {DBT_BIN} run --profiles-dir .",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {ENV} {DBT_BIN} test --profiles-dir .",
    )

    load(extract()) >> dbt_run >> dbt_test