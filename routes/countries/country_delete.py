from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection

countries_delete_router = APIRouter()


@countries_delete_router.delete("/countries/{country_to_delete}")
def delete_entry(country_to_delete: str):
    """
    Supprime une entrée de la base de données pour le pays spécifié.

    Args:
        country_to_delete (str): Le nom du pays à supprimer de la base de données.

    Returns:
        dict: Un dictionnaire contenant le nombre total de requêtes de suppression effectuées
        et un message de confirmation.

    Raises:
        HTTPException(422): Si une erreur se produit lors de la suppression de l'entrée.
    """

    try:
        request_counts['delete_entry'] += 1

        # Établir une connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Insérer le nouveau code de pays et son nom dans la table des pays
        query = f"DELETE FROM countries WHERE name = '{country_to_delete}'"
        cursor.execute(query)
        db.commit()

        # Fermer la connexion à la base de données
        cursor.close()
        db.close()

        return {"request_count": request_counts['delete_entry'],
                "message": f"Entrée avec le nom '{country_to_delete}' supprimée avec succès!"}
    except Exception as e:
        error_message = f"Erreur lors de la suppression de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
