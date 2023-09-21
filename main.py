from fastapi import FastAPI
from routes.weathers import weather_add, weather_get, weather_date, weather_delete, weather_precipitation, \
    weather_temperature, weather_update, weather_statistics
from routes.cities import city_add, city_delete, city_name, city_update, city_weathers, city_statistics
from routes.countries import country_add, country_delete, country_get, country_name, country_statistics, country_update
from routes import root
app = FastAPI()


#Contries


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


#Cities

cities_add_router = city_add.cities_add_router
cities_delete_router = city_delete.cities_delete_router
cities_name_router = city_name.cities_name_router
cities_statistics_router = city_statistics.cities_statistics_router
cities_update_router = city_update.cities_update_router
city_weathers_router = city_weathers.cities_weathers_router


app.include_router(cities_add_router)
app.include_router(cities_delete_router)
app.include_router(cities_name_router)
app.include_router(cities_statistics_router)
app.include_router(cities_update_router)
app.include_router(city_weathers_router)



#Weathers

weathers_add_router = weather_add.weathers_add_router
weathers_get_router = weather_get.weathers_data_router
weathers_date_router = weather_date.weathers_date_router
weathers_delete_router = weather_delete.weathers_delete_router
weathers_precipitation_router = weather_precipitation.weathers_precipitation_router
weathers_temperature_router = weather_temperature.weathers_temperature_router
weathers_update_router = weather_update.weathers_update_router

weather_statistics_router = weather_statistics.weather_statistics_router

app.include_router(weathers_add_router)
app.include_router(weathers_get_router)
app.include_router(weathers_date_router)
app.include_router(weathers_delete_router)
app.include_router(weathers_precipitation_router)
app.include_router(weathers_temperature_router)
app.include_router(weathers_update_router)
app.include_router(weather_statistics_router)

#Root

root_router = root.root_router

app.include_router(root_router)