from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from connectiondb import get_database_connection

cities_router = APIRouter()


# Définir le modèle Pydantic pour la requête entrante
class City(BaseModel):
    name: str


@cities_router.post("/countries/cities/{country_name}")
def create_city_for_country(country_name: str, city: City):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Obtenir l'ID du pays à partir du nom du pays
        country_query = "SELECT id FROM countries WHERE names = %s"
        cursor.execute(country_query, (country_name,))

        country_data = cursor.fetchone()
        if not country_data:
            raise HTTPException(status_code=404, detail=f"Pays nommé {country_name} non trouvé.")

        country_id = country_data[0]

        # Insérer la nouvelle ville avec l'id_country approprié
        city_insert_query = "INSERT INTO cities (id,id_country, name) VALUES (%s,%s, %s)"

        cursor.execute(city_insert_query, (city.id, country_id[0], city.name))

        # Valider l'insertion
        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville {city.name} a été ajoutée avec succès au pays {country_name}."}

    except Exception as e:
        error_message = f"Erreur lors de l'ajout de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
