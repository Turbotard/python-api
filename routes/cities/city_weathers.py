from fastapi import APIRouter, HTTPException
from shared import cities_request_counts, global_request_counts
from connectiondb import get_database_connection

cities_weathers_router = APIRouter()


@cities_weathers_router.get("/cities/weathers/{city_name}")
def get_weather_by_city(city_name: str):
    """
    Récupère les données météorologiques pour une ville spécifiée par son nom.

    Cette fonction se connecte à la base de données, recherche une ville par
    son nom et renvoie toutes les données météorologiques associées à cette ville.
    Si la ville ou les données météorologiques ne sont pas trouvées, une exception
    HTTP 404 est levée.

    Args:
        city_name (str): Le nom de la ville pour laquelle les données météorologiques
                         doivent être récupérées.

    Returns:
        dict: Un dictionnaire contenant le nom de la ville et une liste de toutes les
              données météorologiques associées à cette ville.

    Raises:
        HTTPException: Une exception est levée si la ville ou ses données météorologiques
                       ne sont pas trouvées, ou s'il y a une erreur pendant le processus
                       de récupération.
    """

    try:
        cities_request_counts['city_weathers_entry'] += 1
        global_request_counts['Cities_city_weathers_entry'] += 1

        db = get_database_connection()
        cursor = db.cursor()

        # Utilisation de requêtes paramétrées pour obtenir l'ID de la ville
        city_query = "SELECT id FROM cities WHERE name = %s"
        cursor.execute(city_query, (city_name,))

        city_data = cursor.fetchone()
        print(city_data)
        if not city_data:
            raise HTTPException(status_code=404, detail=f"Aucune ville nommée {city_name} trouvée.")

        city_id = city_data[0]

        # Maintenant, récupérons toutes les météos associées à cette ville
        weather_query = "SELECT * FROM weathers WHERE id_city = %s"
        cursor.execute(weather_query, (city_id,))

        weather_data = cursor.fetchall()

        cursor.close()
        db.close()

        if not weather_data:
            raise HTTPException(status_code=404, detail=f"Pas de données météorologiques pour la ville {city_name}.")

        formatted_weather_data = [
            {'id': row[0], 'id_city': row[1], 'date': row[2], 'tmin': row[3], 'tmax': row[4], 'prcp': row[5],
             'snow': row[6], 'snwd': row[7], 'awnd': row[8]}
            for row in weather_data
        ]

        return {"city": city_name, "weathers": formatted_weather_data}

    except Exception as e:
        error_message = f"Erreur lors de la récupération des données météorologiques pour la ville {city_name}: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
