import statistics

from fastapi import FastAPI
from routes.weathers import add, data, date, delete, precipitation, temperature, update
from routes import statistics, root
app = FastAPI()

weathers_add_router = add.weathers_add_router
weathers_data_router = data.weathers_data_router
weathers_date_router = date.weathers_date_router
weathers_delete_router = delete.weathers_delete_router
weathers_precipitation_router = precipitation.weathers_precipitation_router
weathers_temperature_router = temperature.weathers_temperature_router
weathers_update_router = update.weathers_update_router
weather_root_router = root.weather_root_router
weather_statistics_router = statistics.weather_statistics_router

app.include_router(weathers_add_router)
app.include_router(weathers_data_router)
app.include_router(weathers_date_router)
app.include_router(weathers_delete_router)
app.include_router(weathers_precipitation_router)
app.include_router(weathers_temperature_router)
app.include_router(weathers_update_router)
app.include_router(weather_root_router)
app.include_router(weather_statistics_router)
