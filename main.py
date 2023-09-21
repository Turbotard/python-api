from fastapi import FastAPI
from routes.weathers import weather_add, weather_data, weather_date, weather_delete, weather_precipitation, \
    weather_temperature, weather_update, weather_statistics
from routes.cities import city_name, city_add, city_weathers, city_delete, city_update

from routes import root
app = FastAPI()


weathers_router = city_weathers.weathers_router
cities_router = city_name.cities_router
cities_add_router = city_add.cities_router
cities_delete_router = city_delete.cities_router
cities_update_router = city_update.cities_router

app.include_router(cities_router)
app.include_router(cities_add_router)
app.include_router(weathers_router)
app.include_router(cities_delete_router)
app.include_router(cities_update_router)

weathers_add_router = weather_add.weathers_add_router
weathers_data_router = weather_data.weathers_data_router
weathers_date_router = weather_date.weathers_date_router
weathers_delete_router = weather_delete.weathers_delete_router
weathers_precipitation_router = weather_precipitation.weathers_precipitation_router
weathers_temperature_router = weather_temperature.weathers_temperature_router
weathers_update_router = weather_update.weathers_update_router
weather_root_router = root.weather_root_router
weather_statistics_router = weather_statistics.weather_statistics_router

app.include_router(weathers_add_router)
app.include_router(weathers_data_router)
app.include_router(weathers_date_router)
app.include_router(weathers_delete_router)
app.include_router(weathers_precipitation_router)
app.include_router(weathers_temperature_router)
app.include_router(weathers_update_router)
app.include_router(weather_root_router)
app.include_router(weather_statistics_router)
