from fastapi import APIRouter, HTTPException
from shared import request_counts
from api import data

temperature_router = APIRouter()


@temperature_router.get("/countries/cities/weathers/{temp}")
def filter_by_temperature(temp: float, order: str = "asc"):
    """
    Route pour filtrer les données par température triées par rapport à la température minimale.

    Args:
        temp (float): La température à utiliser comme filtre.
        order (str): Trie la valeur soit "asc" pour croissant soit "desc" pour décroissant.

    Returns:
        dict: Le nombre de requêtes traitées et une liste d'entrées de données filtrées en fonction de la température spécifiée.
    """
    try:
        request_counts['filter_by_temperature'] += 1

        filtered_data = []
        for entry in data:
            tmin = entry.get('tmin')
            tmax = entry.get('tmax')
            if tmin is not None and tmax is not None and temp >= tmin and temp <= tmax:
                filtered_data.append(entry)

        sorted_data = sorted(filtered_data, key=lambda x: x["tmin"], reverse=(order == "desc"))

        return {"request_count": request_counts['filter_by_temperature'], "filtered_data": sorted_data}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors du filtrage par température : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
