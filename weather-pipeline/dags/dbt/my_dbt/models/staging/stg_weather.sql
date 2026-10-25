select
    weather_date,
    temperature::numeric(5,2) as temperature_c,
    wind_speed::numeric(5,2)  as wind_speed_kmh,
    pressure::numeric(7,2)    as pressure_hpa,
    loaded_at
from {{ source('raw', 'weather') }}
where weather_date is not null