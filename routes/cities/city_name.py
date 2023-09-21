from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection

cities_name_router = APIRouter()

@cities_name_router.get("/countries/cities/{city_name}")
def get_city_by_name(city_name: str):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Utilisation de requêtes paramétrées pour éviter les injections SQL
        query = "SELECT * FROM cities WHERE name = %s"
        cursor.execute(query, (city_name,))

        data = cursor.fetchone()  # Récupère une seule entrée puisqu'on s'attend à ce qu'un nom de ville soit unique

        cursor.close()
        db.close()

        if not data:
            raise HTTPException(status_code=404, detail=f"Aucune ville nommée {city_name} trouvée.")

        city_data = {'Code City': data[1], 'Name': data[3]}

        return {"city_name": city_data}

    except Exception as e:
        error_message = f"Erreur lors de la recherche par nom de ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
