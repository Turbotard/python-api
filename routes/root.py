from fastapi import APIRouter
from shared import request_counts

root_router = APIRouter()

@root_router.get("/")
def read_root():
    """
    Route d'accueil de l'API.

    Returns:
        dict: Un message de salutation avec le nombre de requêtes traitées.
    """
    request_counts['root'] += 1
    return {"request_count": request_counts['root'], "message": "Bienvenue dans l'API de données météorologiques."}
