from fastapi import APIRouter, HTTPException
from shared import global_request_counts

root_router = APIRouter()

@root_router.get("/")
def read_root():
    """
    Route d'accueil de l'API pour les requêtes GET.

    Returns:
        dict: Un message de salutation avec le nombre de requêtes GET traitées.
    """
    try:
        global_request_counts['Root'] += 1
        return {"global_request_count": global_request_counts['Root'], "message": "Bienvenue dans l'API de données météorologiques (GET)."}

    except Exception as e:
        error_message = f"Erreur lors de la lecture de la route d'accueil (GET) : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
