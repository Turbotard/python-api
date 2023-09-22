from fastapi import APIRouter, HTTPException
from shared import weathers_request_counts, global_request_counts
from connectiondb import get_database_connection

weathers_data_router = APIRouter()

@weathers_data_router.get("/countries/cities/weathers",
    responses={
        404: {"description": "Aucune donnée météorologique trouvée"},
        422: {"description": "Erreur lors de la récupération des données"},
        500: {"description": "Erreur interne du serveur"}
    }
)
def get_all_data():
    """
    Récupère toutes les données météorologiques disponibles.

    Returns:
        dict: Un dictionnaire contenant le nombre de requêtes traitées, les noms de colonnes et la liste de toutes les entrées de données.

    Raises:
        HTTPException:
            - 404 (Not Found): Si aucune donnée météorologique n'est trouvée.
            - 422 (Unprocessable Entity): Si une erreur survient lors de la récupération des données.
            - 500 (Internal Server Error): Si une erreur interne du serveur se produit.
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

        if not all_data:
            raise HTTPException(status_code=404, detail="Aucune donnée météorologique trouvée.")

        # Créez un dictionnaire avec les noms de colonnes comme clés et les données correspondantes
        data_with_columns = [{column_name: value for column_name, value in zip(column_names, row)} for row in all_data]

        return {"weathers_request_count": weathers_request_counts['get_all_data'], "data": data_with_columns}
    except HTTPException as http_err:
        # Capturez les exceptions HTTP personnalisées et réémettez-les telles quelles
        raise http_err
    except Exception as e:
        error_message = f"Erreur lors de la récupération de toutes les données : {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
