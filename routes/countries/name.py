<<<<<<< Updated upstream:routes/countries/name.py
# temperature.py

=======
>>>>>>> Stashed changes:routes/countries/country_name.py
from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import countries_request_counts

countries_name_router = APIRouter()

@countries_name_router.get("/countries/{country_name}")
def get_country_by_name(country_name: str):
    try:
        countries_request_counts['get_by_name'] += 1

        db = get_database_connection()
        cursor = db.cursor()

        # Utilisation de requêtes paramétrées pour éviter les injections SQL
        query = "SELECT * FROM countries WHERE name = %s"
        cursor.execute(query, (country_name,))

        data = cursor.fetchone()  # Récupère une seule entrée puisqu'on s'attend à ce qu'un nom de ville soit unique

        cursor.close()
        db.close()

        if not data:
            raise HTTPException(status_code=404, detail=f"Aucune pays nommée {country_name} trouvée.")

        country_data = {'Code country': data[1], 'Name': data[2]}

        return {"countries_request_count": countries_request_counts['get_by_name'], "country_name": country_data}

    except Exception as e:
        error_message = f"Erreur lors de la recherche par nom de ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
