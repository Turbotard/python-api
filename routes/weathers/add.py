from fastapi import APIRouter, HTTPException
from shared import request_counts
from api import data
from weather_entry import WeatherEntry
import json

add_router = APIRouter()


@add_router.post("/countries/cities/weathers/{id}")
def add_entry(new_entry: WeatherEntry):
    """
    Route pour ajouter une nouvelle entrée de données.

    Args:
        new_entry (WeatherEntry): Les données de la nouvelle entrée.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    try:
        request_counts['add_entry'] += 1
        data.append(new_entry.dict())

        # Enregistrez les données dans le fichier JSON
        with open('../../scriptsapis/rdu-weather-history.json', 'w') as file:
            json.dump(data, file, indent=4)

        return {"request_count": request_counts['add_entry'], "message": "Nouvelle entrée ajoutée avec succès!"}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de l'ajout de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
