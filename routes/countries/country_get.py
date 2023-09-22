from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import countries_request_counts, global_request_counts
countries_get_router = APIRouter()

@countries_get_router.get("/countries")
def get_all_data():
    """
    Récupère toutes les données des pays depuis la base de données.

    Returns:
        dict: Un dictionnaire contenant le nombre de demandes effectuées et les données des pays.

    Raises:
        HTTPException: En cas d'erreur lors de la récupération des données.
    """
    try:
        countries_request_counts['get_all_data'] += 1
        global_request_counts['Countries_get_all_data'] += 1

        # Établir une connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Exécute la requête SQL pour récupérer toutes les données des pays
        query = "SELECT * FROM countries"
        cursor.execute(query)

        column_names = cursor.column_names

        all_data = cursor.fetchall()

        cursor.close()
        db.close()

        # Créer une liste de dictionnaires pour organiser les données avec les noms de colonnes comme clés
        data_with_columns = [{column_name: value for column_name, value in zip(column_names, row)} for row in all_data]

        return {"countries_request_count": countries_request_counts['get_all_data'], "data": data_with_columns}
    except Exception as e:
        error_message = f"Erreur lors de la récupération de toutes les données : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
