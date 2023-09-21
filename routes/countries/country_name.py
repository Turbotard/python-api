from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import countries_request_counts, global_request_counts

countries_name_router = APIRouter()

@countries_name_router.get("/countries/{name}")
def filter_by_temperature(name: str):
    """
    Endpoint permettant de filtrer des données de pays par nom.

    Args:
        name (str): Le nom du pays à filtrer.

    Returns:
        dict: Un dictionnaire contenant les données filtrées sous la clé "filtered_data".

    Raises:
        HTTPException: En cas d'erreur lors du traitement de la requête, une exception HTTP
        avec le code d'erreur 422 est levée, et les détails de l'erreur sont inclus dans la réponse.
    """
    try:
        countries_request_counts['get_by_name'] += 1
        global_request_counts['Countries_get_by_name'] += 1

        db = get_database_connection()
        cursor = db.cursor()

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM countries WHERE name = %s"
        cursor.execute(query, (name,))

        # Récupérez les données de la base de données
        data = cursor.fetchone()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        # Transformez les résultats en un format approprié (par exemple, liste de dictionnaires)
        formatted_data = [{'id': data[0], 'code_country': data[1], 'name': data[2]}]

        return { "filtered_data": formatted_data}
    except Exception as e:
        error_message = f"Erreur lors du filtrage par nom : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)