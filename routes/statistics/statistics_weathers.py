from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts

statistics_weather_router = APIRouter()


@statistics_weather_router.get("/statistics/weathers",
                               responses={
                                   200: {
                                       "description": "Statistiques récupérées avec succès",
                                       "content": {
                                           "application/json": {
                                               "example": {
                                                   "Statistics": "Weathers",
                                                   "request_count_all_data": 123,
                                                   "request_count_filter_by_date": 45,
                                               }
                                           }
                                       }
                                   },
                                   404: {"description": "statistics non trouvées ou pas de données pour weathers"},
                                   422: {
                                       "description": "Erreur lors de la récupération des statistiques",
                                       "content": {
                                           "application/json": {
                                               "example": {
                                                   "detail": "Erreur inattendue lors de la récupération des statistiques."
                                               }
                                           }
                                       }
                                   },
                                   500: {"description": "Erreur interne du serveur"},

                               }

                               )
def stats():
    """
    Route qui affiche le nombre de requêtes faites pour chaque route.

    Returns:
        dict: Un dictionnaire contenant les compteurs d'utilisation de chaque route.
    Raises:
        HTTPException:
            - 404 (Not Found): Si les stats ne sont pas trouvées dans la base de données.
            - 422 (Unprocessable Entity): Si une erreur survient lors du filtrage par précipitations.
            - 500 (Internal Server Error): Si une erreur interne du serveur se produit.
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
            "request_count_update_entry": weathers_request_counts['update_entry'],
            "request_count_patch_entry": weathers_request_counts['patch_entry']
        }
    except KeyError as e:
        # Handle the KeyError (e.g., key not found in cities_request_counts)
        error_message = f"Clé introuvable dans cities_request_counts : {str(e)}"
        raise HTTPException(status_code=404, detail=error_message)
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
