from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection

cities_name_router = APIRouter()

@cities_name_router.get("/countries/cities/name/{name}")
def get_city_by_name(name: str):
    """
    Récupère les détails d'une ville spécifiée par son nom.

    Cette fonction se connecte à la base de données, recherche une ville
    par son nom et renvoie les détails de la ville si elle est trouvée.
    Sinon, une exception HTTP 404 est levée.

    Args:
        name (str): Le nom de la ville à rechercher.

    Returns:
        dict: Un dictionnaire contenant le code de la ville et son nom
              s'il est trouvé.

    Raises:
        HTTPException: Une exception est levée si la ville n'est pas trouvée
                       ou s'il y a une erreur pendant le processus de recherche.
    """

    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Utilisation de requêtes paramétrées pour éviter les injections SQL
        query = "SELECT * FROM cities WHERE name = %s"
        cursor.execute(query, (name,))

        data = cursor.fetchone()  # Récupère une seule entrée puisqu'on s'attend à ce qu'un nom de ville soit unique

        cursor.close()
        db.close()

        if not data:
            raise HTTPException(status_code=404, detail=f"Aucune ville nommée {name} trouvée.")

        city_data = {'Code City': data[1], 'Name': data[3]}

        return {"city_name": city_data}

    except Exception as e:
        error_message = f"Erreur lors de la recherche par nom de ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
