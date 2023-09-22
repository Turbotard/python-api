from fastapi import APIRouter, HTTPException
from connectiondb import get_database_connection
from shared import countries_request_counts, global_request_counts

countries_name_router = APIRouter()


@countries_name_router.get("/countries/{name}",
                           response_model=dict,
                           # Optionnel : Vous pouvez définir un modèle de réponse précis si nécessaire.
                           responses={
                               200: {
                                   "description": "Données du pays filtrées par nom récupérées avec succès.",
                                   "content": {
                                       "application/json": {
                                           "example": {
                                               "filtered_data": [
                                                   {
                                                       "id": 1,
                                                       "code_country": "FR",
                                                       "name": "France"
                                                   }
                                               ]
                                           }
                                       }
                                   }
                               },
                               404: {
                                   "description": "Aucun pays correspondant au nom fourni n'a été trouvé.",
                                   "content": {
                                       "application/json": {
                                           "example": {
                                               "detail": "Country with name 'NomInexistant' not found."
                                           }
                                       }
                                   }
                               },
                               422: {
                                   "description": "Erreur lors de la récupération des données filtrées.",
                                   "content": {
                                       "application/json": {
                                           "example": {
                                               "detail": "Erreur inattendue lors de la récupération des données filtrées."
                                           }
                                       }
                                   }
                               }
                           })
def get_by_name(name: str):
    """
    Endpoint permettant de filtrer des données de pays par nom.

    Args:
        name (str): Le nom du pays à filtrer.

    Returns:
        dict: Un dictionnaire contenant les données filtrées sous la clé "filtered_data".

    Raises:
        HTTPException: En cas d'erreur lors du traitement de la requête, une exception HTTP
        avec le code d'erreur 422 est levée, et les détails de l'erreur sont inclus dans la réponse.
    """
    try:
        countries_request_counts['get_by_name'] += 1
        global_request_counts['Countries_get_by_name'] += 1

        db = get_database_connection()
        cursor = db.cursor()

        # Exécutez une requête SQL pour récupérer les données filtrées
        query = f"SELECT * FROM countries WHERE name = %s"
        cursor.execute(query, (name,))

        # Récupérez les données de la base de données
        data = cursor.fetchone()

        # Fermez la connexion à la base de données
        cursor.close()
        db.close()
        if data is None:
            raise HTTPException(status_code=404, detail=f"Country with name '{name}' not found.")
        # Transformez les résultats en un format approprié (par exemple, liste de dictionnaires)
        formatted_data = [{'id': data[0], 'code_country': data[1], 'name': data[2]}]

        return {"filtered_data": formatted_data}
    except Exception as e:
        error_message = f"Erreur lors du filtrage par nom : {str(e)}"
        raise HTTPException(status_code=422, detail=error_message)
