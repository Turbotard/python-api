from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts
from connectiondb import get_database_connection  # Importez la fonction pour la connexion à la base de données

weathers_date_router = APIRouter()


@weathers_date_router.get("/countries/cities/weathers/{start_date}/{end_date}")
def filter_by_date(start_date: str, end_date: str, order: str = "asc"):
    """
    Filtre les données météorologiques par plage de dates.

    Args:
        start_date (str): La date de début au format 'YYYY-MM-DD'.
        end_date (str): La date de fin au format 'YYYY-MM-DD'.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et une liste d'entrées de données comprises entre les dates spécifiées.

    Raises:
        HTTPException: Si une erreur survient lors du filtrage par date.
    """
    try:
        weathers_request_counts['filter_by_date'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM weathers WHERE date BETWEEN '{start_date}' AND '{end_date}' ORDER BY date {'DESC' if order == 'desc' else 'ASC'}"
        cursor.execute(query)

        # Récupérez les données de la base de données
        data = cursor.fetchall()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        # Transformez les résultats en un format approprié (par exemple, liste de dictionnaires)
        formatted_data = [
            {'id': row[0], 'id_city': row[1], 'date': row[2], 'tmin': row[3], 'tmax': row[4], 'prcp': row[5],
             'snow': row[6], 'snwd': row[7], 'awnd': row[8]} for row in data]

        return {"weathers_request_count": weathers_request_counts['filter_by_date'], "filtered_data": formatted_data}
    except Exception as e:
        error_message = f"Erreur lors du filtrage par date : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
