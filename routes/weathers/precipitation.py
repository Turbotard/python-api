from typing import Optional
from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection  # Importez la fonction pour la connexion à la base de données

weathers_precipitation_router = APIRouter()


@weathers_precipitation_router.get("/countries/cities/weathers/precipitation/{min_prcp}/{max_prcp}")
def filter_by_precipitation(min_prcp: Optional[float] = None, max_prcp: Optional[float] = None, order: str = "asc"):
    """
    Filtrer les données météorologiques par plage de précipitations.

    Args:
        min_prcp (float, optional): La valeur minimale des précipitations en pouces.
        max_prcp (float, optional): La valeur maximale des précipitations en pouces.
        order (str): Trie la valeur soit "asc" pour croissant soit "desc" pour décroissant.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et une liste d'entrées de données filtrées en fonction des précipitations spécifiées.

    Raises:
        HTTPException: Si une erreur survient lors du filtrage par précipitations.
    """
    try:
        request_counts['filter_by_precipitation'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Construisez la requête SQL en fonction des paramètres min_prcp et max_prcp
        if min_prcp is None:
            min_prcp_condition = ""
        else:
            min_prcp_condition = f"prcp >= {min_prcp}"

        if max_prcp is None:
            max_prcp_condition = ""
        else:
            max_prcp_condition = f"prcp <= {max_prcp}"

        if min_prcp_condition and max_prcp_condition:
            where_clause = f"WHERE {min_prcp_condition} AND {max_prcp_condition}"
        elif min_prcp_condition:
            where_clause = f"WHERE {min_prcp_condition}"
        elif max_prcp_condition:
            where_clause = f"WHERE {max_prcp_condition}"
        else:
            where_clause = ""

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM weathers {where_clause} ORDER BY prcp {'DESC' if order == 'desc' else 'ASC'}"
        cursor.execute(query)

        # Récupérez les données de la base de données
        data = cursor.fetchall()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        return {"request_count": request_counts['filter_by_precipitation'], "filtered_data": data}
    except Exception as e:
        error_message = f"Erreur lors du filtrage par précipitations : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
