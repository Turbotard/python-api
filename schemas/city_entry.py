from pydantic import BaseModel


class CityEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'une entrée météorologique.

    Attributes:
    """
    code_city: str
    name: str
