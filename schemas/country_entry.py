from pydantic import BaseModel

class CountryEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'un pays.

    Attributes:
        code_country (str): Le code du pays.
        name (str): Le nom du pays.
    """
    code_country: str
    name: str
