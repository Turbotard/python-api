from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection

weathers_date_router = APIRouter()

@weathers_date_router.get("/countries/cities/weathers/date",
    responses={
        400: {"description": "Format incorrect"},
        422: {"description": "Erreur lors du filtrage"},
        500: {"description": "Erreur interne du serveur"}
    })
def filter_by_date(
    start_date: str = Query(None, description="La date de début au format 'YYYY-MM-DD'."),
    end_date: str = Query(None, description="La date de fin au format 'YYYY-MM-DD'."),
    order: str = Query("asc", description="L'ordre de tri ('asc' pour croissant ou 'desc' pour décroissant).")
):
    """
    Filtre les données météorologiques par plage de dates.

    Args:
        start_date (str): La date de début au format 'YYYY-MM-DD'.
        end_date (str): La date de fin au format 'YYYY-MM-DD'.
        order (str): L'ordre de tri ('asc' pour croissant ou 'desc' pour décroissant).

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et une liste d'entrées de données comprises entre les dates spécifiées.

    Raises:
        HTTPException:
            - 400 (Bad Request): Si les dates spécifiées sont dans un format incorrect.
            - 422 (Unprocessable Entity): Si une erreur survient lors du filtrage par date.
            - 500 (Internal Server Error): Si une erreur inattendue se produit.
    """
    try:
        # Vérifiez si les dates sont au format correct
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date incorrect. Utilisez 'YYYY-MM-DD'.")

        weathers_request_counts['filter_by_date'] += 1
        global_request_counts['Weathers_filter_by_date'] += 1

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
    except HTTPException as http_err:
        # Capturez les exceptions HTTP personnalisées et réémettez-les telles quelles
        raise http_err
    except Exception as e:
        error_message = f"Erreur lors du filtrage par date : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
