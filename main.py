from fastapi import FastAPI
from routes.cities import city_name, city_add, city_weathers, city_delete, city_update
from routes.weathers import temperature

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