select *
from {{ ref('stg_weather') }}
where temperature_c not between -60 and 60
   or pressure_hpa  not between 850 and 1100
   or wind_speed_kmh < 0