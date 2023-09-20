from fastapi import FastAPI
from routes.weathers import temperature

app = FastAPI()


temperature_router = temperature.temperature_router



app.include_router(temperature_router)






