from fastapi import APIRouter, HTTPException
from schemas.country_entry import CountryEntry
from connectiondb import get_database_connection
from share import countries_request_counts


countries_add_router = APIRouter()

@countries_add_router.post("/countries")
def add_country_entry(new_entry: CountryEntry):
    """
    Ajoute une nouvelle entrée de pays à la base de données.

    Args:
        new_entry (CountryEntry): Les données de la nouvelle entrée de pays.

    Returns:
        dict: Un dictionnaire contenant le nombre total de demandes d'ajout d'entrée de pays
        jusqu'à présent et un message de confirmation.

    Raises:
        HTTPException (status_code=422): En cas d'erreur lors de l'ajout de l'entrée de pays,
        renvoie une exception HTTP avec un code d'état 422 et un message d'erreur détaillé.
    """
    try:
        countries_request_counts['add_entry'] += 1

        # Établir une connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Insérer le nouveau code de pays et son nom dans la table des pays
        query = "INSERT INTO countries (code_country, name) VALUES (%s, %s)"
        data = (new_entry.code_country,
                new_entry.name)
        cursor.execute(query, data)
        db.commit()

        # Fermer la connexion à la base de données
        cursor.close()
        db.close()

        return {"countries_request_count": countries_request_counts['add_entry'], "message": "Nouvelle entrée de pays ajoutée avec succès!"}
    except Exception as e:
        error_message = f"Erreur lors de l'ajout de l'entrée de pays : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
