<<<<<<< Updated upstream
import statistics

from fastapi import FastAPI
from routes.countries import country_add, country_get, country_delete, country_update
from routes.weathers import add, data, date, delete, precipitation, temperature, update
from routes import statistics, root
=======
from fastapi import FastAPI
from routes.weathers import weather_add, weather_data, weather_date, weather_delete, weather_precipitation, \
    weather_temperature, weather_update, weather_statistics
from routes.cities import city_add, city_delete, city_name, city_update, city_weathers
from routes.countries import country_add, country_delete, country_get, country_name, country_statistics, country_update
from routes import root
>>>>>>> Stashed changes
app = FastAPI()

countries_add_router = country_add.countries_add_router
countries_get_router = country_get.countries_get_router
countries_delete_router = country_delete.countries_delete_router
countries_update_router = country_update.countries_update_router

<<<<<<< Updated upstream
app.include_router(countries_add_router)
app.include_router(countries_get_router)
app.include_router(countries_delete_router)
app.include_router(countries_update_router)

weathers_add_router = add.weathers_add_router
weathers_data_router = data.weathers_data_router
weathers_date_router = date.weathers_date_router
weathers_delete_router = delete.weathers_delete_router
weathers_precipitation_router = precipitation.weathers_precipitation_router
weathers_temperature_router = temperature.weathers_temperature_router
weathers_update_router = update.weathers_update_router
weather_root_router = root.weather_root_router
weather_statistics_router = statistics.weather_statistics_router
=======
city_add_router = city_add.cities_add_router
city_delete_router = city_delete.cities_delete_router
city_name_router = city_name.cities_name_router
city_update_router = city_update.cities_update_router
city_weathers_router = city_weathers.cities_weathers_router

app.include_router(city_add_router)
app.include_router(city_delete_router)
app.include_router(city_name_router)
app.include_router(city_update_router)
app.include_router(city_weathers_router)


country_add_router = country_add.countries_add_router
country_delete_router = country_delete.countries_delete_router
country_get_router = country_get.countries_get_router
country_name_router = country_name.countries_name_router
country_statistics_router = country_statistics.countries_statistics_router
country_update_router = country_update.countries_update_router

app.include_router(country_add_router)
app.include_router(country_delete_router)
app.include_router(country_get_router)
app.include_router(country_name_router)
app.include_router(country_statistics_router)
app.include_router(country_update_router)


weathers_add_router = weather_add.weathers_add_router
weathers_data_router = weather_data.weathers_data_router
weathers_date_router = weather_date.weathers_date_router
weathers_delete_router = weather_delete.weathers_delete_router
weathers_precipitation_router = weather_precipitation.weathers_precipitation_router
weathers_statistics_router = weather_statistics.weathers_statistics_router
weathers_temperature_router = weather_temperature.weathers_temperature_router
weathers_update_router = weather_update.weathers_update_router
>>>>>>> Stashed changes

app.include_router(weathers_add_router)
app.include_router(weathers_data_router)
app.include_router(weathers_date_router)
app.include_router(weathers_delete_router)
app.include_router(weathers_precipitation_router)
app.include_router(weathers_statistics_router)
app.include_router(weathers_temperature_router)
app.include_router(weathers_update_router)


root_router = root.root_router
app.include_router(root_router)


