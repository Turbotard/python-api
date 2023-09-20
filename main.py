from fastapi import FastAPI
from routes.cities import weathers_city
from routes.cities import name, add
from routes.weathers import temperature

app = FastAPI()

weathers_router = weathers_city.weathers_router
cities_router = name.cities_router
citiesadd_router = add.cities_router
temperature_router = temperature.temperature_router

app.include_router(temperature_router)
app.include_router(cities_router)
app.include_router(citiesadd_router)
app.include_router(weathers_router)
