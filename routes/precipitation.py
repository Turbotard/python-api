from typing import Optional

from fastapi import APIRouter
from shared import request_counts
from api import data

precipitation_router = APIRouter()

@precipitation_router.get("/data/filter-by-precipitation")
def filter_by_precipitation(min_prcp: Optional[float] = None, max_prcp: Optional[float] = None, order: str = "asc"):
    """
    Route pour filtrer les données par plage de précipitations.

    Args:
        min_prcp (float, optional): La valeur minimale des précipitations en pouces.
        max_prcp (float, optional): La valeur maximale des précipitations en pouces.
        order (string): trie la valeure soit asc pour croissant soit desc pour décroissant
    Returns:
        dict: Le nombre de requêtes traitées et une liste d'entrées de données filtrées en fonction des précipitations spécifiées.
    """
    request_counts['filter_by_precipitation'] += 1
    if min_prcp is None and max_prcp is None:
        return {"request_count": request_counts['filter_by_precipitation'], "data": data}

    filtered_data = []

    for entry in data:
        prcp = entry.get('prcp')
        if prcp is not None and (min_prcp is None or prcp >= min_prcp) and (max_prcp is None or prcp <= max_prcp):
            filtered_data.append(entry)
    sorted_data = sorted(filtered_data, key=lambda x: x["prcp"], reverse=(order == "desc"))
    return {"request_count": request_counts['filter_by_precipitation'], "filtered_data": sorted_data}