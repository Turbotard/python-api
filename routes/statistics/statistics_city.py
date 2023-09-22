from fastapi import APIRouter, HTTPException
from shared import cities_request_counts

statistics_cities_router = APIRouter()

@statistics_cities_router.get("/statistics/cities")
def stats():
    """
    Route qui affiche le nombre de requêtes faites pour chaque route.

    Returns:
        dict: Un dictionnaire contenant les compteurs d'utilisation de chaque route.
    """
    try:
        return {
            "Statistics": "City",
            "request_count_add": cities_request_counts['add_entry'],
            "request_count_delete": cities_request_counts['delete_entry'],
            "request_count_name": cities_request_counts['name_entry'],
            "request_count_update": cities_request_counts['update_entry'],
            "request_count_city_weathers": cities_request_counts['city_weathers_entry']
        }
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
