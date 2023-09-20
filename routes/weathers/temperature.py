# temperature.py

from fastapi import APIRouter, HTTPException
from shared import request_counts
from connectiondb import get_database_connection  # Importez la fonction depuis database.py

temperature_router = APIRouter()

# Modifiez votre route pour utiliser la base de données
@temperature_router.get("/countries/cities/weathers/{temp}")
def filter_by_temperature(temp: float, order: str = "asc"):
    try:
        request_counts['filter_by_temperature'] += 1

        # Établissez la connexion à la base de données en utilisant la fonction du fichier database.py
        db = get_database_connection()
        cursor = db.cursor()

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM weathers WHERE tmin <= {temp} AND tmax >= {temp} ORDER BY tmin {'DESC' if order == 'desc' else 'ASC'}"
        cursor.execute(query)

        # Récupérez les données de la base de données
        data = cursor.fetchall()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        # Transformez les résultats en un format approprié (par exemple, liste de dictionnaires)
        formatted_data = [{'id': row[0], 'id_city': row[1], 'date': row[2], 'tmin': row[3], 'tmax': row[4], 'prcp': row[5], 'snow': row[6], 'snwd': row[7], 'awnd': row[8]} for row in data]

        return {"request_count": request_counts['filter_by_temperature'], "filtered_data": formatted_data}
    except Exception as e:
        error_message = f"Erreur lors du filtrage par température : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
