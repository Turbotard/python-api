from fastapi import APIRouter, HTTPException
from shared import cities_request_counts, global_request_counts
from connectiondb import get_database_connection
from schemas.city_entry import CityEntry

cities_update_router = APIRouter()

@cities_update_router.put(
    "/countries/cities/{old_code_city}",
    response_model=dict,  # Vous pouvez également spécifier un modèle Pydantic plus spécifique ici
    responses={
        404: {"description": "Ville non trouvée"},
        409: {"description": "Le nouveau code postal existe déjà"},
        422: {"description": "Erreur lors de la mise à jour de la ville ou paramètres non valides"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def update_city_by_code(old_code_city: str, updated_entry: CityEntry):
    """
    Met à jour les informations d'une ville en utilisant son code postal.

    Cette fonction reçoit le code postal actuel d'une ville et les nouvelles
    informations sous forme d'une entrée "CityEntry". Elle vérifie d'abord si la ville
    avec ce code postal existe. Si elle existe, la fonction met à jour les informations
    de la ville en utilisant les données fournies dans "updated_entry". Si le code postal
    spécifié dans "updated_entry" est différent de "old_code_city" et qu'il existe déjà
    dans la base de données, une exception HTTP 409 est levée.

    Args:
        old_code_city (str): Le code postal actuel de la ville à mettre à jour.
        updated_entry (CityEntry): Les nouvelles informations pour la ville.

    Returns:
        dict: Un dictionnaire contenant le statut de la mise à jour et un message.

    Raises:
        HTTPException:
            - 404 (Not Found): Si aucune ville avec le code postal spécifié n'est trouvée.
            - 409 (Conflict): Si le nouveau code postal existe déjà.
            - 422 (Unprocessable Entity): Si une erreur survient lors de la mise à jour de la ville.
            - 500 (Internal Server Error): Si une erreur interne du serveur se produit.
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

        # Check if the new postal code already exists, only if it's different from the old one
        if old_code_city != updated_entry.code_city:
            check_new_code_query = "SELECT id FROM cities WHERE code_city = %s"
            cursor.execute(check_new_code_query, (updated_entry.code_city,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail=f"Le code postal {updated_entry.code_city} existe déjà.")

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

    except HTTPException as he:
        raise he
    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
