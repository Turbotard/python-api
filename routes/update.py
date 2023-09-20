from fastapi import APIRouter, HTTPException
from shared import request_counts
import json
from weather_entry import WeatherEntry
from api import data

update_router = APIRouter()


@update_router.put("/countries/cities/weathers/{date_to_update}")
def update_entry(updated_entry: WeatherEntry):
    """
    Route pour mettre à jour une entrée de données par date.

    Args:
        updated_entry (WeatherEntry): Les données mises à jour de l'entrée.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    try:
        request_counts['update_entry'] += 1

        date_to_update = updated_entry.date

        # Mettre à jour l'entrée de données correspondante ou ajouter une nouvelle entrée si elle n'existe pas
        updated_data = []
        updated = False
        for entry in data:
            if entry['date'] == date_to_update:
                updated_data.append(updated_entry.dict())
                updated = True
            else:
                updated_data.append(entry)

        if not updated:
            updated_data.append(updated_entry.dict())

        # Enregistrez les données mises à jour dans le fichier JSON
        with open('../scriptsapis/rdu-weather-history.json', 'w') as file:
            json.dump(updated_data, file, indent=4)

        return {"request_count": request_counts['update_entry'],
                "message": f"Entrée avec date {date_to_update} mise à jour avec succès!"}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la mise à jour de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
