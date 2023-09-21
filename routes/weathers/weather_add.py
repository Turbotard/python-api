from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection  # Importez la fonction pour la connexion à la base de données
from weather_entry import WeatherEntry

weathers_add_router = APIRouter()

@weathers_add_router.post("/countries/cities/weathers/{name_city}")
def add_entry(name_city: str, new_entry: WeatherEntry):
    """
    Ajoute une nouvelle entrée de données météorologiques.

    Args:
        name_city (str): Le nom de la ville associée à l'entrée météorologique.
        new_entry (WeatherEntry): Les données de la nouvelle entrée.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées et un message de confirmation.

    Raises:
        HTTPException: Si une erreur survient lors de l'ajout de l'entrée.
    """
    try:
        request_counts['add_entry'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Recherchez l'ID de la ville en fonction du nom de la ville
        query = "SELECT id FROM cities WHERE name = %s"
        cursor.execute(query, (name_city,))
        city_id = cursor.fetchone()

        if city_id:
            # Si l'ID de la ville existe, insérez les données dans la table weathers
            query = """
            INSERT INTO weathers (id_city, date, tmin, tmax, prcp, snow, snwd, awnd)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                city_id[0],  # Utilisez l'ID de la ville obtenu
                new_entry.date,
                new_entry.tmin,
                new_entry.tmax,
                new_entry.prcp,
                new_entry.snow,
                new_entry.snwd,
                new_entry.awnd,
            )
            cursor.execute(query, data)
            db.commit()

            # Fermez la connexion à la base de données
            cursor.close()
            db.close()

            return {"request_count": request_counts['add_entry'], "message": "Nouvelle entrée ajoutée avec succès!"}
        else:
            raise HTTPException(status_code=404, detail="Ville non trouvée dans la base de données.")
    except Exception as e:
        error_message = f"Erreur lors de l'ajout de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
