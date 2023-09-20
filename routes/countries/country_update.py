from fastapi import APIRouter, HTTPException

from schemas.country_entry import CountryEntry
from shared import request_counts
from connectiondb import get_database_connection  # Importez la fonction pour la connexion à la base de données
from schemas.weather_entry import WeatherEntry

countries_update_router = APIRouter()

@countries_update_router.put("/countries/{country_to_update}")
def update_entry(country_to_update: str, updated_entry: CountryEntry):
    """
    Mettre à jour ou ajouter une entrée de pays dans la base de données.

    Args:
        country_to_update (str): Le nom du pays à mettre à jour ou à ajouter.
        updated_entry (CountryEntry): Les données mises à jour pour le pays.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes effectuées et un message de succès ou d'erreur.

    Raises:
        HTTPException: Si une erreur survient lors de la mise à jour ou de l'ajout de l'entrée de pays.

    Example:
        Pour mettre à jour ou ajouter des données pour le pays "France" avec les données de pays suivantes :
        {
            "code_country": "FR",
            "name": "France"
        }
        Utilisez une requête PUT avec les données JSON correspondantes.

    """

    try:
        request_counts['update_entry'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Mettez à jour l'entrée de données correspondante ou ajoutez une nouvelle entrée si elle n'existe pas
        query = f"SELECT * FROM countries WHERE name = '{country_to_update}'"
        cursor.execute(query)
        existing_data = cursor.fetchone()

        if existing_data:
            # Mettre à jour l'entrée existante avec la nouvelle date
            query = """
            UPDATE countries
            SET code_country = %s, name = %s
            WHERE name = %s
            """
            data = (updated_entry.code_country,
                    updated_entry.name, country_to_update)

            cursor.execute(query, data)
        else:
            # Ajouter une nouvelle entrée
            query = """
            INSERT INTO countries (code_country, name)
            VALUES (%s, %s)
            """
            data = (updated_entry.code_country,
                    updated_entry.name)
            cursor.execute(query, data)

        db.commit()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        return {"request_count": request_counts['update_entry'],
                "message": f"Entrée avec date {country_to_update} mise à jour avec succès!"}
    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de l'entrée : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
