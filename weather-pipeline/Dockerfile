FROM astrocrpublic.azurecr.io/runtime:3.3-9

RUN python -m venv /usr/local/airflow/dbt_venv && \
    /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-postgres

RUN pip install --no-cache-dir uv && \
    uv venv --python 3.12 /usr/local/airflow/dbt_venv312 && \
    uv pip install --python /usr/local/airflow/dbt_venv312/bin/python dbt-postgres
