from fastapi import FastAPI
from routes import root, statistics
from routes.weathers import add, data, date, delete, precipitation, temperature, update

app = FastAPI()

add_router = add.add_router
data_router = data.data_router
date_router = date.date_router
delete_router = delete.delete_router
precipitation_router = precipitation.precipitation_router
root_router = root.root_router
statistics_router = statistics.statistics_router
temperature_router = temperature.temperature_router
update_router = update.update_router


app.include_router(add_router)
app.include_router(data_router)
app.include_router(date_router)
app.include_router(delete_router)
app.include_router(precipitation_router)
app.include_router(root_router)
app.include_router(statistics_router)
app.include_router(temperature_router)
app.include_router(update_router)






