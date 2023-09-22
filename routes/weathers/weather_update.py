from fastapi import APIRouter, HTTPException, status
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection
from schemas.weather_entry import WeatherEntry

weathers_update_router = APIRouter()

@weathers_update_router.put("/countries/cities/weathers/{date_to_update}",
    responses={
        404: {"description": "Date à mettre à jour non trouvée dans la base de données"},
        409: {"description": "Une entrée existe déjà pour cette ville à cette date lors de la mise à jour."},
        422: {"description": "Erreur lors de la mise à jour de l'entrée"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def update_entry(date_to_update: str, updated_entry: WeatherEntry):
    """
    Met à jour une entrée de données météorologiques par date ou ajoute une nouvelle entrée si elle n'existe pas.

    Args:
        date_to_update (str): La date de l'entrée à mettre à jour au format 'YYYY-MM-DD'.
        updated_entry (WeatherEntry): Les données mises à jour de l'entrée.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et un message de confirmation.

    Raises:
        HTTPException:
            - 404 (Not Found): Si la date à mettre à jour n'est pas trouvée dans la base de données.
            - 409 (Conflict): Si une entrée avec la même date existe déjà dans la ville spécifiée lors de la mise à jour.
            - 422 (Unprocessable Entity): Si une erreur survient lors de la mise à jour de l'entrée.
            - 500 (Internal Server Error): Si une erreur interne du serveur se produit.
    """
    try:
        weathers_request_counts['update_entry'] += 1
        global_request_counts['Weathers_update_entry'] += 1

        # Établir la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Vérifier s'il existe déjà une entrée pour la ville spécifiée à cette date
        query = """
        SELECT id FROM weathers WHERE id_city = %s AND date = %s
        """
        cursor.execute(query, (updated_entry.id_city, updated_entry.date))
        existing_entry = cursor.fetchone()

        if existing_entry:
            raise HTTPException(status_code=409, detail="Une entrée existe déjà pour cette ville à cette date lors de la mise à jour.")

        # Mettre à jour l'entrée de données correspondante ou ajouter une nouvelle entrée si elle n'existe pas
        query = f"SELECT * FROM weathers WHERE date = '{date_to_update}'"
        cursor.execute(query)
        existing_data = cursor.fetchone()

        if existing_data:
            # Mettre à jour l'entrée existante avec la nouvelle date
            query = """
            UPDATE weathers
            SET id_city = %s, date = %s, tmin = %s, tmax = %s, prcp = %s, snow = %s, snwd = %s, awnd = %s
            WHERE date = %s
            """
            data = (
                updated_entry.id_city,
                updated_entry.date,  # Utilisez la nouvelle date ici
                updated_entry.tmin,
                updated_entry.tmax,
                updated_entry.prcp,
                updated_entry.snow,
                updated_entry.snwd,
                updated_entry.awnd,
                date_to_update,  # Utilisez l'ancienne date ici
            )
            cursor.execute(query, data)
        else:
            # Ajouter une nouvelle entrée
            query = """
            INSERT INTO weathers (id_city, date, tmin, tmax, prcp, snow, snwd, awnd)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                updated_entry.id_city,
                updated_entry.date,  # Utilisez la nouvelle date ici
                updated_entry.tmin,
                updated_entry.tmax,
                updated_entry.prcp,
                updated_entry.snow,
                updated_entry.snwd,
                updated_entry.awnd,
            )
            cursor.execute(query, data)

        db.commit()

        # Fermer la connexion à la base de données
        cursor.close()
        db.close()

        return {"weathers_request_count": weathers_request_counts['update_entry'],
                "message": f"Entrée avec date {date_to_update} mise à jour avec succès!"}
    except HTTPException as http_exception:
        # Si une HTTPException est levée, la renvoyer directement
        raise http_exception
    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de l'entrée : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
