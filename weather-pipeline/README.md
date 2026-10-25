# Weather pipeline: Airflow + dbt + PostgreSQL

Учебный ETL-проект. Каждый день Airflow забирает данные о погоде из открытого API, загружает их в PostgreSQL, строит витрины с помощью dbt и проверяет качество данных тестами.

## Схема

```
Open-Meteo API -> Airflow (extract, load) -> raw.weather
                                                |
                                  dbt run: stg_weather -> weather_weekly
                                                |
                                          dbt test
```

## Стек

- **Apache Airflow** (Astro CLI): оркестрация, расписание `@daily`, retries
- **dbt (dbt-postgres)**: преобразования и тесты данных
- **PostgreSQL 16**: хранилище (контейнер `dwh`)
- **Docker**: запуск всего окружения
- **Python**: `requests`, `PostgresHook`

## Что делает пайплайн

DAG `weather_load` состоит из четырёх задач:

1. `extract`: запрашивает у Open-Meteo среднюю температуру, максимальную скорость ветра и среднее давление за последние 7 дней и сегодня.
2. `load`: записывает данные в `raw.weather`. Загрузка **идемпотентна** (первичный ключ по дате и `replace`), поэтому повторный запуск не создаёт дубликатов.
3. `dbt_run`: строит модели.
4. `dbt_test`: проверяет данные.

## Модели dbt

| Модель | Слой | Описание |
|---|---|---|
| `stg_weather` | staging (view) | типы данных и понятные названия колонок с единицами измерения |
| `weather_weekly` | marts (table) | средняя температура, максимальный ветер и среднее давление по неделям |
| `customer_totals` | marts | вспомогательная учебная модель по таблице `raw.orders` |

Тесты: `unique` и `not_null` на ключах и показателях, а также собственный тест `weather_values_in_range` (правдоподобные диапазоны температуры, давления и ветра).

## Структура проекта

```
dags/
  weather_dag.py        # DAG: загрузка + dbt run + dbt test
  dbt/my_dbt/           # dbt-проект
    models/
      sources.yml
      schema.yml
      staging/stg_weather.sql
      marts/weather_weekly.sql
    tests/weather_values_in_range.sql
    profiles.yml.example
Dockerfile              # dbt в отдельном окружении (Python 3.12)
docker-compose.override.yml  # контейнер с PostgreSQL
requirements.txt
```

## Как запустить

1. Установите Docker Desktop (на Windows с WSL2) и [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli).
2. Скопируйте профиль dbt и поставьте свой пароль:
```bash
   cp dags/dbt/my_dbt/profiles.yml.example dags/dbt/my_dbt/profiles.yml
```
   Логин и пароль должны совпадать с `POSTGRES_USER` и `POSTGRES_PASSWORD` в `docker-compose.override.yml`.
3. Запустите окружение:
```bash
   astro dev start
```
4. В интерфейсе Airflow создайте подключение **Admin -> Connections -> Add**: Connection Id `dwh`, тип Postgres, Host `dwh`, Port `5432`, Database `dbt_demo`, логин и пароль из шага 2.
5. Запустите DAG `weather_load` кнопкой Trigger.
6. Посмотрите результат (например, в DBeaver: `localhost:5433`, база `dbt_demo`):
```sql
   SELECT * FROM analytics.weather_weekly;
```

Остановить: `astro dev stop`.

