from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts
from connectiondb import get_database_connection

weathers_delete_router = APIRouter()

@weathers_delete_router.delete("/countries/cities/weathers/{name_city}/{date_to_delete}")
def delete_entry(name_city: str, date_to_delete: str):
    """
    Supprime une entrée de données météorologiques par date pour une ville donnée.

    Args:
        name_city (str): Le nom de la ville associée à l'entrée météorologique.
        date_to_delete (str): La date de l'entrée à supprimer au format 'YYYY-MM-DD'.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et un message de confirmation.

    Raises:
        HTTPException: Si une erreur survient lors de la suppression de l'entrée ou si la ville n'est pas trouvée.
    """
    try:
        weathers_request_counts['delete_entry'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Recherchez l'ID de la ville en fonction du nom de la ville
        query = "SELECT id FROM cities WHERE name = %s"
        cursor.execute(query, (name_city,))
        city_id = cursor.fetchone()

        if city_id:
            # Supprimez l'entrée de données avec la date spécifiée et l'ID de la ville correspondant
            query = "DELETE FROM weathers WHERE id_city = %s AND date = %s"
            cursor.execute(query, (city_id[0], date_to_delete))
            db.commit()

            # Fermez la connexion à la base de données
            cursor.close()
            db.close()

            return {"request_count": weathers_request_counts['delete_entry'],
                    "message": f"Entrée avec date {date_to_delete} pour la ville {name_city} supprimée avec succès!"}
        else:
            raise HTTPException(status_code=404, detail="Ville non trouvée dans la base de données.")
    except Exception as e:
        error_message = f"Erreur lors de la suppression de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
