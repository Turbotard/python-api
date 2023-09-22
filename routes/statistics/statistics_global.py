from fastapi import APIRouter, HTTPException
from shared import global_request_counts, global_request_counts, global_request_counts, global_request_counts

statistics_router = APIRouter()


@statistics_router.get("/statistics",
                       responses={
                           200: {"description": "Statistiques récupérées avec succès",
                                 "content": {"application/json": {"example": {
                                     "Statistics 1": "Root",
                                     "request_count_root": 123,
                                 }}}
                                 },
                           404: {"description": "statistics non trouvées ou pas de données en global"},
                           422: {"description": "Erreur lors de la récupération des statistiques",
                                 "content": {"application/json": {"example": {
                                     "detail": "Erreur inattendue lors de la récupération des statistiques."}}}
                                 },
                           500: {"description": "Erreur interne du serveur"},

                       })
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
            "Statistics 1": "Root",
            "request_count_root": global_request_counts['Root'],
            "Statistics 2": "City",
            "Cities_request_count_add": global_request_counts['Cities_add_entry'],
            "Cities_request_count_delete": global_request_counts['Cities_delete_entry'],
            "Cities_request_count_name": global_request_counts['Cities_name_entry'],
            "Cities_request_count_update": global_request_counts['Cities_update_entry'],
            "Cities_request_count_city_weathers": global_request_counts['Cities_city_weathers_entry'],
            "Statistics 3": "Countries",
            "Countries_request_count_add_entry": global_request_counts['Countries_add_entry'],
            "Countries_request_count_delete_entry": global_request_counts['Countries_delete_entry'],
            "Countries_request_count_all_data": global_request_counts['Countries_get_all_data'],
            "Countries_request_count_get_by_name": global_request_counts['Countries_get_by_name'],
            "Countries_request_count_update_entry": global_request_counts['Countries_update_entry'],
            "Statistics 4": "Weathers",
            "Weathers_request_count_all_data": global_request_counts['Weathers_get_all_data'],
            "Weathers_request_count_filter_by_date": global_request_counts['Weathers_filter_by_date'],
            "Weathers_request_count_filter_by_precipitation": global_request_counts['Weathers_filter_by_precipitation'],
            "Weathers_request_count_filter_by_temperature": global_request_counts['Weathers_filter_by_temperature'],
            "Weathers_request_count_add_entry": global_request_counts['Weathers_add_entry'],
            "Weathers_request_count_delete_entry": global_request_counts['Weathers_delete_entry'],
            "Weathers_request_count_update_entry": global_request_counts['Weathers_update_entry']
        }
    except KeyError as e:
        # Handle the KeyError (e.g., key not found in cities_request_counts)
        error_message = f"Clé introuvable dans cities_request_counts : {str(e)}"
        raise HTTPException(status_code=404, detail=error_message)
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
