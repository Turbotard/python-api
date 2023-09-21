from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection  # Importez la fonction pour la connexion à la base de données
from schemas.weather_entry import WeatherEntry

weathers_update_router = APIRouter()

@weathers_update_router.put("/countries/cities/weathers/{date_to_update}")
def update_entry(date_to_update: str, updated_entry: WeatherEntry):
    """
    Met à jour une entrée de données météorologiques par date ou ajoute une nouvelle entrée si elle n'existe pas.

    Args:
        date_to_update (str): La date de l'entrée à mettre à jour au format 'YYYY-MM-DD'.
        updated_entry (WeatherEntry): Les données mises à jour de l'entrée.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et un message de confirmation.

    Raises:
        HTTPException: Si une erreur survient lors de la mise à jour de l'entrée.
    """
    try:
        request_counts['update_entry'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Mettez à jour l'entrée de données correspondante ou ajoutez une nouvelle entrée si elle n'existe pas
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

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        return {"request_count": request_counts['update_entry'],
                "message": f"Entrée avec date {date_to_update} mise à jour avec succès!"}
    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
