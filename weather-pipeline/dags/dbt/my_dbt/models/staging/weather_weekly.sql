{{ config(materialized='table') }}

select
    date_trunc('week', weather_date)::date as week_start,
    round(avg(temperature_c), 1)           as avg_temperature_c,
    max(wind_speed_kmh)                    as max_wind_speed_kmh,
    round(avg(pressure_hpa), 1)            as avg_pressure_hpa,
    count(*)                               as days_count
from {{ ref('stg_weather') }}
group by 1
order by 1