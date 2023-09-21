from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection

cities_delete_router = APIRouter()
@cities_delete_router.delete("/cities/delete/{code_city}")
def delete_city_by_code(code_city: str):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        # Vérifier si la ville avec ce code postal existe
        check_query = "SELECT id FROM cities WHERE code_city = %s"
        cursor.execute(check_query, (code_city,))
        city_data = cursor.fetchone()

        if not city_data:
            raise HTTPException(status_code=404, detail=f"Ville avec le code postal {code_city} non trouvée.")

        # Supprimer la ville avec le code postal donné
        delete_query = "DELETE FROM cities WHERE code_city = %s"
        cursor.execute(delete_query, (code_city,))

        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville avec le code postal {code_city} a été supprimée avec succès."}

    except Exception as e:
        error_message = f"Erreur lors de la suppression de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)