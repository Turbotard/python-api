from fastapi import APIRouter, HTTPException
from shared import countries_request_counts

statistics_countries_router = APIRouter()

@statistics_countries_router.get(
    "/statistics/countries/",
    responses={
        200: {"description": "Statistiques récupérées avec succès",
              "content": {"application/json": {"example": {
                  "Statistics": "Countries",
                  "request_count_add_entry": 100,
                  "request_count_delete_entry": 50,
                  "request_count_all_data": 250,
                  "request_count_get_by_name": 120,
                  "request_count_update_entry": 90
              }}}
        },
        404: {"description": "statistics non trouvées ou pas de données pour ce pays"},
        422: {"description": "Erreur lors de la récupération des statistiques",
              "content": {"application/json": {"example": {"detail": "Erreur inattendue lors de la récupération des statistiques."}}}
        },
        500: {"description": "Erreur interne du serveur"},
    }
)
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
    except KeyError as e:
        # Handle the KeyError (e.g., key not found in cities_request_counts)
        error_message = f"Clé introuvable dans cities_request_counts : {str(e)}"
        raise HTTPException(status_code=404, detail=error_message)
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la récupération des statistiques : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
