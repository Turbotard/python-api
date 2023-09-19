from fastapi import APIRouter
from shared import request_counts
from api import data
from weather_entry import WeatherEntry
import json


add_router = APIRouter()

@add_router.post("/data/add-entry")
def add_entry(new_entry: WeatherEntry):
    """
    Route pour ajouter une nouvelle entrée de données.

    Args:
        new_entry (WeatherEntry): Les données de la nouvelle entrée.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    request_counts['add_entry'] += 1
    data.append(new_entry.dict())
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"request_count": request_counts['add_entry'], "message": "Nouvelle entrée ajoutée avec succès!"}
