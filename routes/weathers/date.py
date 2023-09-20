from datetime import datetime

from fastapi import APIRouter, HTTPException
from shared import request_counts
from api import data

date_router = APIRouter()


@date_router.get("/countries/cities/weathers/{start_date}/{end_date}")
def filter_by_date(start_date: str, end_date: str, order: str = "asc"):
    """
    Route pour filtrer les données par plage de dates.

    Args:
        start_date (str): La date de début au format 'YYYY-MM-DD'.
        end_date (str): La date de fin au format 'YYYY-MM-DD'.

    Returns:
        dict: Le nombre de requêtes traitées et une liste d'entrées de données comprises entre les dates spécifiées.
    """
    try:
        request_counts['filter_by_date'] += 1

        # Convertir les dates en objets datetime
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        # Filtrer les données en fonction de la plage de dates
        filtered_data = [entry for entry in data if
                         start_datetime <= datetime.strptime(entry['date'], "%Y-%m-%d") <= end_datetime]

        # Trier les données en fonction de l'ordre spécifié
        sorted_data = sorted(filtered_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
                             reverse=(order == "desc"))

        return {"request_count": request_counts['filter_by_date'], "filtered_data": sorted_data}
    except Exception as e:
        # Gérez l'exception et renvoyez une réponse d'erreur appropriée
        error_message = f"Erreur lors du filtrage par date : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
