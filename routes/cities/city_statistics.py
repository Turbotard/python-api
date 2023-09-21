from fastapi import APIRouter, HTTPException

from city_share import city_request_counts

cities_statistics_router = APIRouter()

@cities_statistics_router.get("/cities/statistics")
def stats():
    """
    Route qui affiche le nombre de requêtes faites pour chaque route.

    Returns:
        dict: Un dictionnaire contenant les compteurs d'utilisation de chaque route.
    """
    try:
        return {
            "Statistics": "City",
            "request_count_add": city_request_counts['add_entry'],
            "request_count_delete": city_request_counts['delete_entry'],
            "request_count_name": city_request_counts['name_entry'],
            "request_count_update": city_request_counts['update_entry'],
            "request_count_city_weathers": city_request_counts['city_weathers_entry']
        }
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)