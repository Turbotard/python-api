from fastapi import APIRouter
from shared import request_counts
import json
from weather_entry import WeatherEntry

from api import data

update_router = APIRouter()


@update_router.put("/countries/cities/weathers/{id}")
def update_entry(updated_entry: WeatherEntry):
    """
    Route pour mettre à jour une entrée de données par date.

    Args:
        updated_entry (WeatherEntry): Les données mises à jour de l'entrée.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    request_counts['update_entry'] += 1
    date_to_update = updated_entry.date
    data[:] = [entry if entry['date'] != date_to_update else updated_entry.dict() for entry in data]
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"request_count": request_counts['update_entry'],
            "message": f"Entrée avec date {date_to_update} mise à jour avec succès!"}
