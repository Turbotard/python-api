from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection

weathers_data_router = APIRouter()

@weathers_data_router.get("/countries/cities/weathers")
def get_all_data():
    """
    Récupère toutes les données météorologiques disponibles.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées, les noms de colonnes et la liste de toutes les entrées de données.

    Raises:
        HTTPException: Si une erreur survient lors de la récupération des données.
    """
    try:
        weathers_request_counts['get_all_data'] += 1
        global_request_counts['Weathers_get_all_data'] += 1

        # Établissez la connexion à la base de données
        db = get_database_connection()
        cursor = db.cursor()

        # Exécutez une requête SQL pour récupérer toutes les données
        query = "SELECT * FROM weathers"
        cursor.execute(query)

        # Récupérez les noms de colonnes
        column_names = cursor.column_names

        # Récupérez toutes les données météorologiques
        all_data = cursor.fetchall()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()

        # Créez un dictionnaire avec les noms de colonnes comme clés et les données correspondantes
        data_with_columns = [{column_name: value for column_name, value in zip(column_names, row)} for row in all_data]

        return {"weathers_request_count": weathers_request_counts['get_all_data'], "data": data_with_columns}
    except Exception as e:
        error_message = f"Erreur lors de la récupération de toutes les données : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
