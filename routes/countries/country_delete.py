from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import countries_request_counts, global_request_counts

countries_delete_router = APIRouter()


@countries_delete_router.delete("/countries/{country_to_delete}",
                                response_model=dict,
                                # Optionnel : Vous pouvez définir un modèle de réponse précis si nécessaire.
                                responses={
                                    200: {
                                        "description": "Entrée de pays supprimée avec succès",
                                        "content": {
                                            "application/json": {
                                                "example": {
                                                    "countries_request_count": 1,
                                                    "message": "Entrée avec le nom 'France' supprimée avec succès!"
                                                }
                                            }
                                        }
                                    },
                                    422: {
                                        "description": "Erreur lors de la suppression de l'entrée",
                                        "content": {
                                            "application/json": {
                                                "example": {
                                                    "detail": "Erreur inattendue lors de la suppression de l'entrée."
                                                }
                                            }
                                        }
                                    }
                                })
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
        countries_request_counts['delete_entry'] += 1
        global_request_counts['Countries_delete_entry'] += 1

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

        return {"countries_request_count": countries_request_counts['delete_entry'],
                "message": f"Entrée avec le nom '{country_to_delete}' supprimée avec succès!"}
    except Exception as e:
        error_message = f"Erreur lors de la suppression de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
