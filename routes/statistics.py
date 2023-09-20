from fastapi import APIRouter, HTTPException
from shared import request_counts

weather_statistics_router = APIRouter()

@weather_statistics_router.get("/statistics")
def stats():
    """
    Route qui affiche le nombre de requêtes faites pour chaque route.

    Returns:
        dict: Un dictionnaire contenant les compteurs d'utilisation de chaque route.
    """
    try:
        return {
            "request_count_root": request_counts['root'],
            "request_count_all_data": request_counts['get_all_data'],
            "request_count_filter_by_date": request_counts['filter_by_date'],
            "request_count_filter_by_precipitation": request_counts['filter_by_precipitation'],
            "request_count_filter_by_temperature": request_counts['filter_by_temperature'],
            "request_count_add_entry": request_counts['add_entry'],
            "request_count_delete_entry": request_counts['delete_entry'],
            "request_count_update_entry": request_counts['update_entry']
        }
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
