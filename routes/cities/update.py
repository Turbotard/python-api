from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from connectiondb import get_database_connection

cities_router = APIRouter()

class CityUpdate(BaseModel):
    code_cities: str
    name: str

@cities_router.put("/cities/update/{old_code_cities}")
def update_city_by_code(old_code_cities: str, city_update: CityUpdate = Body(...)):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Vérifier si la ville avec ce code postal existe
        check_query = "SELECT id FROM cities WHERE code_cities = %s"
        cursor.execute(check_query, (old_code_cities,))
        city_data = cursor.fetchone()

        if not city_data:
            raise HTTPException(status_code=404, detail=f"Ville avec le code postal {old_code_cities} non trouvée.")

        # Mettre à jour la ville avec les nouvelles données
        update_query = "UPDATE cities SET code_cities = %s, name = %s WHERE code_cities = %s"
        cursor.execute(update_query, (city_update.code_cities, city_update.name, old_code_cities))

        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville avec le code postal {old_code_cities} a été mise à jour avec succès."}

    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
