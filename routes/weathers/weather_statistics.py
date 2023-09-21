from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts

weathers_statistics_router = APIRouter()

@weathers_statistics_router.get("/weathers/statistics")
def stats():
    """
    Route qui affiche le nombre de requêtes faites pour chaque route.

    Returns:
        dict: Un dictionnaire contenant les compteurs d'utilisation de chaque route.
    """
    try:
        return {
            "Statistics": "Weathers",
            "request_count_all_data": weathers_request_counts['get_all_data'],
            "request_count_filter_by_date": weathers_request_counts['filter_by_date'],
            "request_count_filter_by_precipitation": weathers_request_counts['filter_by_precipitation'],
            "request_count_filter_by_temperature": weathers_request_counts['filter_by_temperature'],
            "request_count_add_entry": weathers_request_counts['add_entry'],
            "request_count_delete_entry": weathers_request_counts['delete_entry'],
            "request_count_update_entry": weathers_request_counts['update_entry']
        }
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
