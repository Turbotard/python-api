from fastapi import APIRouter, HTTPException
from shared import countries_request_counts

statistics_countries_router = APIRouter()

@statistics_countries_router.get("/statistics/countries/")
def stats():
    """
    Route qui affiche le nombre de requêtes faites pour chaque route.

    Returns:
        dict: Un dictionnaire contenant les compteurs d'utilisation de chaque route.
    """
    try:
        return {
            "Statistics": "Countries",
            "request_count_add_entry": countries_request_counts['add_entry'],
            "request_count_delete_entry": countries_request_counts['delete_entry'],
            "request_count_all_data": countries_request_counts['get_all_data'],
            "request_count_get_by_name": countries_request_counts['get_by_name'],
            "request_count_update_entry": countries_request_counts['update_entry']
        }
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
