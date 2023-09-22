from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from shared import cities_request_counts, global_request_counts
from connectiondb import get_database_connection

cities_name_router = APIRouter()

@cities_name_router.get(
    "/countries/cities",
    response_model=dict,
    responses={
        404: {"description": "Ville non trouvée"},
        422: {"description": "Erreur lors de la recherche de la ville ou paramètres non valides"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def get_city_by_name(city_name: Optional[str] = Query(None, description="Le nom de la ville à rechercher.")):
    """
    Récupère les détails d'une ville spécifiée par son nom.

    Cette fonction se connecte à la base de données, recherche une ville
    par son nom et renvoie les détails de la ville si elle est trouvée.
    Sinon, une exception HTTP 404 est levée.

    Args:
        city_name (str, optional): Le nom de la ville à rechercher.

    Returns:
        dict: Un dictionnaire contenant le code de la ville et son nom
              s'il est trouvé.

    Raises:
        HTTPException: Une exception est levée si la ville n'est pas trouvée
                       ou s'il y a une erreur pendant le processus de recherche.
    """

    if city_name is None:
        raise HTTPException(status_code=422, detail="Veuillez fournir un nom de ville.")

    try:
        cities_request_counts['name_entry'] += 1
        global_request_counts['Cities_name_entry'] += 1

        db = get_database_connection()
        cursor = db.cursor()

        # Utilisation de requêtes paramétrées pour éviter les injections SQL
        query = "SELECT * FROM cities WHERE name = %s"
        cursor.execute(query, (city_name,))

        data = cursor.fetchone()

        cursor.close()
        db.close()

        if not data:
            raise HTTPException(status_code=404, detail=f"Ville nommée {city_name} non trouvée.")

        city_data = {'Code City': data[1], 'Name': data[3]}

        return {"city_name": city_data}

    except HTTPException:
        raise
    except Exception as e:
        error_message = f"Erreur lors de la recherche par nom de ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
