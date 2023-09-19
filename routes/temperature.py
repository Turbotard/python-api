from fastapi import APIRouter
from shared import request_counts
from api import data

temperature_router = APIRouter()


@temperature_router.get("/countries/cities/weathers/{temp}")
def filter_by_precipitation(temp: float, order: str = "asc"):
    """
    Route pour filtrer les données par température trié par rapport au min

    Args:
        temp: (float) Temparature
        order (string): trie la valeure soit asc pour croissant soit desc pour décroissant

    Returns:
        dict : les températurs filtrés entre tmin et tmax
    """
    request_counts['filter_by_temperature'] += 1
    filtered_data = []
    for entry in data:
        tmin = entry.get('tmin')
        tmax = entry.get('tmax')
        if temp >= tmin and temp <= tmax:
            filtered_data.append(entry)
    sorted_data = sorted(filtered_data, key=lambda x: x["tmin"], reverse=(order == "desc"))
    return {"request_count": request_counts['filter_by_temperature'], "filtered_data": sorted_data}
