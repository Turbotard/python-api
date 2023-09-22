from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection
from schemas.weather_entry import WeatherEntry

weathers_add_router = APIRouter()

@weathers_add_router.post("/countries/cities/weathers/{name_city}", responses={
        404: {"description": "Ville non trouvée"},
        409: {"description": "Le relevé existe déjà pour cette ville"},
        422: {"description": "Erreur lors de l'ajout du relevé ou paramètres non valides"},
        500: {"description": "Erreur interne du serveur"}
    })
def add_entry(name_city: str, new_entry: WeatherEntry):
    try:
        weathers_request_counts['add_entry'] += 1
        global_request_counts['Weathers_add_entry'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Recherchez l'ID de la ville en fonction du nom de la ville
        query = "SELECT id FROM cities WHERE name = %s"
        cursor.execute(query, (name_city,))
        city_id = cursor.fetchone()

        if city_id:
            # Vérifiez s'il existe déjà un relevé pour cette ville à cette date
            query = """
            SELECT id FROM weathers WHERE id_city = %s AND date = %s
            """
            cursor.execute(query, (city_id[0], new_entry.date))
            existing_entry = cursor.fetchone()

            if existing_entry:
                raise HTTPException(status_code=409, detail="Un relevé existe déjà pour cette ville à cette date.")

            # Si l'ID de la ville existe et qu'aucun relevé n'existe pour cette date, insérez les données
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

            return {"weathers_request_count": weathers_request_counts['add_entry'],
                    "message": "Nouvelle entrée ajoutée avec succès!"}
        else:
            raise HTTPException(status_code=404, detail="Ville non trouvée dans la base de données.")
    except HTTPException as http_exception:
        # Si une HTTPException est levée, la renvoyer directement
        raise http_exception
    except Exception as e:
        # Si une autre exception inattendue se produit, renvoyer une HTTPException avec le détail de l'erreur
        error_message = f"Erreur lors de l'ajout de l'entrée : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
