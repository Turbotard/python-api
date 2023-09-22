from fastapi import APIRouter, HTTPException
from shared import cities_request_counts, global_request_counts
from connectiondb import get_database_connection
from schemas.city_entry import CityEntry

cities_update_router = APIRouter()

@cities_update_router.put("/countries/cities/{old_code_city}")
def update_city_by_code(old_code_city: str, updated_entry: CityEntry):
    """
    Mise à jour des détails d'une ville spécifiée par son code postal.

    Cette fonction se connecte à la base de données, vérifie si une ville avec le
    code postal spécifié existe. Si elle existe, elle est mise à jour avec les nouvelles
    informations fournies. Sinon, une exception HTTP 404 est levée.

    Args:
        old_code_city (str): Le code postal de la ville à mettre à jour.
        updated_entry (CityEntry): Un objet Pydantic contenant les détails mis à jour
                                   de la ville, y compris le nouveau code postal et le nom.

    Returns:
        dict: Un dictionnaire contenant le statut (success ou failure) et un message
              décrivant le résultat de l'opération.

    Raises:
        HTTPException: Une exception est levée si la ville n'est pas trouvée ou s'il y a
                       une erreur pendant le processus de mise à jour.
    """
    try:
        cities_request_counts['update_entry'] += 1
        global_request_counts['Cities_update_entry'] += 1

        db = get_database_connection()
        cursor = db.cursor()

        # Check if the city with this postal code exists
        check_query = "SELECT id FROM cities WHERE code_city = %s"
        cursor.execute(check_query, (old_code_city,))
        city_data = cursor.fetchone()

        if not city_data:
            raise HTTPException(status_code=404, detail=f"Ville avec le code postal {old_code_city} non trouvée.")

        # Update the city with the new data
        update_query = """
            UPDATE cities 
            SET code_city = %s, name = %s 
            WHERE code_city = %s
            """
        cursor.execute(update_query, (updated_entry.code_city, updated_entry.name, old_code_city))

        db.commit()

        cursor.close()
        db.close()

        return {"status": "success",
                "message": f"La ville avec le code postal {old_code_city} a été mise à jour avec succès."}

    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)

