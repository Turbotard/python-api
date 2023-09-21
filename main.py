from fastapi import FastAPI
from routes.cities import city_name, city_add, city_weathers, city_delete, city_update
from routes.weathers import temperature

app = FastAPI()

weathers_router = weathers_city.weathers_router
cities_router = name.cities_router
cities_add_router = add.cities_router
cities_delete_router = delete.cities_router
cities_update_router = update.cities_router

app.include_router(cities_router)
app.include_router(cities_add_router)
app.include_router(weathers_router)
app.include_router(cities_delete_router)
app.include_router(cities_update_router)