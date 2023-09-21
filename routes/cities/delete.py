from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from connectiondb import get_database_connection

cities_router = APIRouter()
@cities_router.delete("/cities/delete/{code_cities}")
def delete_city_by_code(code_cities: str):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Vérifier si la ville avec ce code postal existe
        check_query = "SELECT id FROM cities WHERE code_cities = %s"
        cursor.execute(check_query, (code_cities,))
        city_data = cursor.fetchone()

        if not city_data:
            raise HTTPException(status_code=404, detail=f"Ville avec le code postal {code_cities} non trouvée.")

        # Supprimer la ville avec le code postal donné
        delete_query = "DELETE FROM cities WHERE code_cities = %s"
        cursor.execute(delete_query, (code_cities,))

        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville avec le code postal {code_cities} a été supprimée avec succès."}

    except Exception as e:
        error_message = f"Erreur lors de la suppression de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
