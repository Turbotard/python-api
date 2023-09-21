from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import countries_request_counts

countries_name_router = APIRouter()

@countries_name_router.get("/countries/name/{name}")
def get_city_by_name(name: str):
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

        db = get_database_connection()
        cursor = db.cursor()

        # Utilisation de requêtes paramétrées pour éviter les injections SQL
        query = "SELECT * FROM countries WHERE name = %s"
        cursor.execute(query, (name,))

        data = cursor.fetchone()  # Récupère une seule entrée puisqu'on s'attend à ce qu'un nom de pays soit unique

        cursor.close()
        db.close()

        if not data:
            raise HTTPException(status_code=404, detail=f"Aucun pays nommé {name} trouvée.")

        city_data = {'Code Country': data[1], 'Name': data[2]}

        return {"countries_request_count": countries_request_counts['get_by_name'], "city_name": city_data}

    except Exception as e:
        error_message = f"Erreur lors de la recherche par nom du pays : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)


