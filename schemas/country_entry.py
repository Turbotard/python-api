from pydantic import BaseModel
from typing import Optional


class CountryEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'un pays.

    Attributes:
    """
    code_country: str
    name: str
