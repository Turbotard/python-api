from fastapi import APIRouter
from shared import request_counts
from api import data

data_router = APIRouter()


@data_router.get("countries/cities/weathers")
def get_all_data():
    """
    Route pour consulter toutes les données météorologiques.

    Returns:
        dict: Le nombre de requêtes traitées et une liste de toutes les entrées de données.
    """
    request_counts['get_all_data'] += 1
    return {"request_count": request_counts['get_all_data'], "data": data}
