from fastapi import APIRouter, HTTPException
from shared import request_counts

root_router = APIRouter()

@root_router.get("/")
def read_root():
    """
    Route d'accueil de l'API.

    Returns:
        dict: Un message de salutation avec le nombre de requêtes traitées.
    """
    try:
        request_counts['root'] += 1
        return {"request_count": request_counts['root'], "message": "Bienvenue dans l'API de données météorologiques."}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors de la lecture de la route d'accueil : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
