from fastapi import FastAPI
from routes.weathers import temperature
from routes.countries import name

app = FastAPI()

countries_name_router = name.countries_name_router
temperature_router = temperature.temperature_router


app.include_router(countries_name_router)
app.include_router(temperature_router)






