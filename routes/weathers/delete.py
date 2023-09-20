from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection  # Importez la fonction pour la connexion à la base de données

weathers_delete_router = APIRouter()


@weathers_delete_router.delete("/countries/cities/weathers/{date_to_delete}")
def delete_entry(date_to_delete: str):
    """
    Supprime une entrée de données météorologiques par date.

    Args:
        date_to_delete (str): La date de l'entrée à supprimer au format 'YYYY-MM-DD'.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et un message de confirmation.

    Raises:
        HTTPException: Si une erreur survient lors de la suppression de l'entrée.
    """
    try:
        request_counts['delete_entry'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Supprimez l'entrée de données avec la date spécifiée
        query = f"DELETE FROM weathers WHERE date = '{date_to_delete}'"
        cursor.execute(query)
        db.commit()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        return {"request_count": request_counts['delete_entry'],
                "message": f"Entrée avec date {date_to_delete} supprimée avec succès!"}
    except Exception as e:
        error_message = f"Erreur lors de la suppression de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
