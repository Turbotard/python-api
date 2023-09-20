from fastapi import APIRouter, HTTPException
from shared import request_counts
from api import data
import json

delete_router = APIRouter()


@delete_router.delete("/countries/cities/weathers/{date_to_delete}")
def delete_entry(date_to_delete: str):
    """
    Route pour supprimer une entrée de données par date.

    Args:
        date_to_delete (str): La date de l'entrée à supprimer au format 'YYYY-MM-DD'.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    try:
        request_counts['delete_entry'] += 1

        # Supprimer l'entrée de données avec la date spécifiée
        data[:] = [entry for entry in data if entry['date'] != date_to_delete]

        # Enregistrez les données mises à jour dans le fichier JSON
        with open('../scriptsapis/rdu-weather-history.json', 'w') as file:
            json.dump(data, file, indent=4)

        return {"request_count": request_counts['delete_entry'],
                "message": f"Entrée avec date {date_to_delete} supprimée avec succès!"}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la suppression de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
