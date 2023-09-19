from fastapi import APIRouter
from shared import request_counts

statistics_router = APIRouter()


@statistics_router.get("/statistics")
def stats():
    """
    Route qui affiche le nombres de requètes faites pour chaques route
|
    Returns:
        request_count : renvoie des counters des utilisations de chaques routes

    """
    return {"request_count_root": request_counts['root'],
            "request_count_all_data": request_counts['get_all_data'],
            "request_count_filter_by_date": request_counts['filter_by_date'],
            "request_count_filter_by_precipitation": request_counts['filter_by_precipitation'],
            "request_count_filter_by_temperature": request_counts['filter_by_temperature'],
            "request_count_add_entry": request_counts['add_entry'],
            "request_count_delete_entry": request_counts['delete_entry'],
            "request_count_update_entry": request_counts['update_entry']}
