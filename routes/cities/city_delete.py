from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import cities_request_counts, global_request_counts

cities_delete_router = APIRouter()

@cities_delete_router.delete(
    "/countries/cities/{code_city}",
    responses={
        404: {"description": "Ville avec le code postal spécifié non trouvée"},
        422: {"description": "Erreur lors de la suppression de la ville ou paramètres non valides"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def delete_city_by_code(code_city: str):
    """
    Supprime une ville en utilisant son code postal.

    Cette fonction établit une connexion à la base de données et tente de supprimer
    une ville basée sur le code postal spécifié. Si la ville avec le code postal
    donné n'existe pas, une exception est levée pour informer l'utilisateur.

    Args:
        code_city (str): Le code postal de la ville à supprimer.

    Returns:
        dict: Un dictionnaire qui contient deux clés :
              - "status": indiquant le succès ("success") ou l'échec ("failure") de l'opération.
              - "message": fournissant des détails supplémentaires sur le résultat de l'opération.
    """
    try:
        # Incrémenter les compteurs pour suivre le nombre de requêtes
        cities_request_counts['delete_entry'] += 1
        global_request_counts['Cities_delete_entry'] += 1

        # Établir la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Supprimer la ville basée sur le code postal fourni
        delete_query = "DELETE FROM cities WHERE code_city = %s"
        cursor.execute(delete_query, (code_city,))

        # Vérifier si la ville a bien été supprimée. Si aucune ligne n'est affectée, cela signifie que la ville n'existait pas.
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Ville avec le code postal {code_city} n'existe pas.")

        # Valider les changements dans la base de données
        db.commit()

        # Fermer le curseur et la connexion à la base de données
        cursor.close()
        db.close()

        return {"status": "success", "message": f"La ville avec le code postal {code_city} a été supprimée avec succès."}

    except HTTPException:
        # Relancer l'exception si elle est déjà gérée
        raise
    except Exception as e:
        # Gérer toutes les autres exceptions et renvoyer un message d'erreur
        error_message = f"Erreur lors de la suppression de la ville : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
