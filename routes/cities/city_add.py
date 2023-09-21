from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from connectiondb import get_database_connection
from schemas.city_entry import CityEntry

cities_add_router = APIRouter()

# Modifiez le modèle pour inclure le code postale


@cities_add_router.post("/countries/cities/{country_name}")
def create_city_for_country(country_name: str, new_entry: CityEntry):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Récupérez l'ID du pays en utilisant le nom du pays
        country_query = "SELECT id FROM countries WHERE name = %s"
        cursor.execute(country_query, (country_name,))

        country_data = cursor.fetchone()
        if not country_data:
            raise HTTPException(status_code=404, detail=f"Pays nommé {country_name} non trouvé.")

        country_id = country_data[0]

        # Ajustez la requête d'insertion pour la ville
        city_insert_query = "INSERT INTO cities (code_city, id_country, name) VALUES (%s, %s, %s)"

        cursor.execute(city_insert_query, (new_entry.code_city, country_id, new_entry.name))

        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville {new_entry.name} a été ajoutée avec succès au pays {country_name}."}

    except Exception as e:
        error_message = f"Erreur lors de l'ajout de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
