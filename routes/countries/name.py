# weather_temperature.py

from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection

countries_name_router = APIRouter()

@countries_name_router.get("/countries/{name}")
def filter_by_temperature(name: str):
    """
    Retrieve country data by name.

    Args:
        name (str): The name of the country to filter.

    Returns:
        dict: A dictionary containing the filtered country data, e.g., {"filtered_data": [{"id": 1, "name": "France"}]}.

    Raises:
        HTTPException: If an error occurs during the database query.
    """
    try:

        db = get_database_connection()
        cursor = db.cursor()

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM countries WHERE names = %s"
        cursor.execute(query, (name,))

        # Récupérez les données de la base de données
        data = cursor.fetchone()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        # Transformez les résultats en un format approprié (par exemple, liste de dictionnaires)
        formatted_data = [{'id': data[0], 'names': data[1]}]

        return { "filtered_data": formatted_data}
    except Exception as e:
        error_message = f"Erreur lors du filtrage par nom : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
