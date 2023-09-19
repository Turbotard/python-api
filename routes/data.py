from fastapi import APIRouter, HTTPException
from shared import request_counts
from api import data

data_router = APIRouter()


@data_router.get("/countries/cities/weathers")
def get_all_data():
    """
    Route pour consulter toutes les données météorologiques.

    Returns:
        dict: Le nombre de requêtes traitées et une liste de toutes les entrées de données.
    """
    try:
        request_counts['get_all_data'] += 1

        # Récupérez toutes les données météorologiques
        all_data = data  # Assurez-vous que 'data' est une liste contenant toutes vos données

        return {"request_count": request_counts['get_all_data'], "data": all_data}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération de toutes les données : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
