from datetime import datetime

from fastapi import APIRouter
from shared import request_counts
from api import data

date_router = APIRouter()


@date_router.get("/countries/cities/weathers/{date}")
def filter_by_date(start_date: str, end_date: str, order: str = "asc"):
    """
    Route pour filtrer les données par plage de dates.

    Args:
        start_date (str): La date de début au format 'YYYY-MM-DD'.
        end_date (str): La date de fin au format 'YYYY-MM-DD'.

    Returns:
        dict: Le nombre de requêtes traitées et une liste d'entrées de données comprises entre les dates spécifiées.
    """
    request_counts['filter_by_date'] += 1
    filtered_data = [entry for entry in data if start_date <= entry['date'] <= end_date]
    sorted_data = sorted(filtered_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
                         reverse=(order == "desc"))

    return {"request_count": request_counts['filter_by_date'], "filtered_data": sorted_data}
