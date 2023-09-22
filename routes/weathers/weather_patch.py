from fastapi import APIRouter, HTTPException, status

from schemas.partial_weather_entry import PartialWeatherEntry
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection
from schemas.weather_entry import WeatherEntry

weathers_patch_router = APIRouter()

@weathers_patch_router.patch("/countries/cities/weathers/{date_to_update}",
    responses={
        404: {"description": "Date à mettre à jour non trouvée dans la base de données"},
        422: {"description": "Erreur lors de la mise à jour de l'entrée"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def patch_entry(date_to_update: str, updated_entry: PartialWeatherEntry):
    try:
        weathers_request_counts['patch_entry'] += 1
        global_request_counts['Weathers_patch_entry'] += 1

        # Établir la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Vérifier si l'entrée existe pour la ville spécifiée à cette date
        query = """
        SELECT id FROM weathers WHERE id_city = %s AND date = %s
        """
        cursor.execute(query, (updated_entry.id_city, date_to_update))
        existing_entry = cursor.fetchone()

        if not existing_entry:
            raise HTTPException(status_code=404, detail="Date à mettre à jour non trouvée dans la base de données.")

        # Construire la clause SET pour la mise à jour en fonction des champs spécifiés dans le corps de la requête
        set_clause = []
        update_data = []

        if updated_entry.tmin is not None:
            set_clause.append("tmin = %s")
            update_data.append(updated_entry.tmin)

        if updated_entry.tmax is not None:
            set_clause.append("tmax = %s")
            update_data.append(updated_entry.tmax)

        if updated_entry.prcp is not None:
            set_clause.append("prcp = %s")
            update_data.append(updated_entry.prcp)

        if updated_entry.snow is not None:
            set_clause.append("snow = %s")
            update_data.append(updated_entry.snow)

        if updated_entry.snwd is not None:
            set_clause.append("snwd = %s")
            update_data.append(updated_entry.snwd)

        if updated_entry.awnd is not None:
            set_clause.append("awnd = %s")
            update_data.append(updated_entry.awnd)

        # Mettre à jour la base de données en utilisant la clause SET construite
        if set_clause:
            set_clause = ", ".join(set_clause)
            query = f"""
            UPDATE weathers
            SET {set_clause}
            WHERE id_city = %s AND date = %s
            """
            update_data.extend([updated_entry.id_city, date_to_update])
            cursor.execute(query, update_data)

            db.commit()

        # Fermer la connexion à la base de données
        cursor.close()
        db.close()

        return {"weathers_request_count": weathers_request_counts['patch_entry'],
                "message": f"Données météorologiques pour la date {date_to_update} mises à jour avec succès!"}
    except HTTPException as http_exception:
        # Si une HTTPException est levée, la renvoyer directement
        raise http_exception
    except Exception as e:
        error_message = f"Erreur lors de la mise à jour de l'entrée : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)

