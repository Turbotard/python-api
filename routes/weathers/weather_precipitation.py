from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection

weathers_precipitation_router = APIRouter()

@weathers_precipitation_router.get("/countries/cities/weathers/precipitation",
    responses={
        422: {"description": "Erreur lors du filtrage par précipitations"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def filter_by_precipitation(
    min_prcp: Optional[float] = Query(None, description="La valeur minimale des précipitations en pouces."),
    max_prcp: Optional[float] = Query(None, description="La valeur maximale des précipitations en pouces."),
    order: str = "asc"
):
    """
    Filtrer les données météorologiques par plage de précipitations.

    Args:
        min_prcp (float, optional): La valeur minimale des précipitations en pouces.
        max_prcp (float, optional): La valeur maximale des précipitations en pouces.
        order (str): Trie la valeur soit "asc" pour croissant soit "desc" pour décroissant.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et une liste d'entrées de données filtrées en fonction des précipitations spécifiées.

    Raises:
        HTTPException:
            - 422 (Unprocessable Entity): Si une erreur survient lors du filtrage par précipitations.
            - 500 (Internal Server Error): Si une erreur interne du serveur se produit.
    """
    try:
        weathers_request_counts['filter_by_precipitation'] += 1
        global_request_counts['Weathers_filter_by_precipitation'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Construisez la requête SQL en fonction des paramètres min_prcp et max_prcp
        conditions = []

        if min_prcp is not None:
            conditions.append(f"prcp >= {min_prcp}")

        if max_prcp is not None:
            conditions.append(f"prcp <= {max_prcp}")

        where_clause = " AND ".join(conditions)

        if where_clause:
            where_clause = "WHERE " + where_clause

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM weathers {where_clause} ORDER BY prcp {'DESC' if order == 'desc' else 'ASC'}"
        cursor.execute(query)

        # Récupérez les données de la base de données
        data = cursor.fetchall()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        return {"weathers_request_count": weathers_request_counts['filter_by_precipitation'], "filtered_data": data}
    except HTTPException as http_err:
        # Capturez les exceptions HTTP personnalisées et réémettez-les telles quelles
        raise http_err
    except Exception as e:
        error_message = f"Erreur lors du filtrage par précipitations : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
