from datetime import datetime

from fastapi import FastAPI
import json

with open('rdu-weather-history.json') as test:
    data = json.load(test)
print(data)

app = FastAPI()


@app.get("/")
async def read_root(order: str = "asc"):
    """

    :param order:
    :return:
    """
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=(order == "desc"))
    return sorted_data

@app.get("/prcp")
async def read_root(order: str = "asc"):
    """

    :param order:
    :return:
    """
    sorted_data = sorted(data, key=lambda x: x["prcp"], reverse=(order == "desc"))
    return sorted_data






