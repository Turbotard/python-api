from fastapi import FastAPI
from routes.cities import name, add, weathers_city
from routes.weathers import temperature

app = FastAPI()

weathers_router = weathers_city.weathers_router
cities_router = name.cities_router
cities_add_router = add.cities_router

app.include_router(cities_router)
app.include_router(cities_add_router)
app.include_router(weathers_router)