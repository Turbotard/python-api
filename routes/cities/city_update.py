from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from connectiondb import get_database_connection
from schemas.city_entry import CityEntry


cities_update_router = APIRouter()

@cities_update_router.put("/cities/update/{old_code_city}")
def update_city_by_code(old_code_city: str, updated_entry: CityEntry):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Vérifier si la ville avec ce code postal existe
        check_query = "SELECT id FROM cities WHERE code_city = %s"
        cursor.execute(check_query, (old_code_city,))
        city_data = cursor.fetchone()

        if not city_data:
            raise HTTPException(status_code=404, detail=f"Ville avec le code postal {old_code_city} non trouvée.")

        # Mettre à jour la ville avec les nouvelles données
        update_query = "UPDATE cities SET code_city = %s, name = %s WHERE code_city = %s"
        cursor.execute(update_query, (updated_entry.code_city, updated_entry.name, old_code_city))

        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville avec le code postal {old_code_city} a été mise à jour avec succès."}

    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
