from fastapi import APIRouter
from shared import request_counts
from api import data
import json

delete_router = APIRouter()


@delete_router.delete("/countries/cities/weathers/{id}")
def delete_entry(date_to_delete: str):
    """
    Route pour supprimer une entrée de données par date.

    Args:
        date_to_delete (str): La date de l'entrée à supprimer au format 'YYYY-MM-DD'.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    request_counts['delete_entry'] += 1
    data[:] = [entry for entry in data if entry['date'] != date_to_delete]
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"request_count": request_counts['delete_entry'],
            "message": f"Entrée avec date {date_to_delete} supprimée avec succès!"}
