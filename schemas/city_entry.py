from pydantic import BaseModel

class CityEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'une ville.

    Attributes:
        code_city (str): Le code de la ville.
        name (str): Le nom de la ville.
    """
    code_city: str
    name: str
