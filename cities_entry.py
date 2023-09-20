from pydantic import BaseModel
from typing import Optional


class CitiesEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'une entrée météorologique.

    Attributes:
    """
    id: int
    id_country: Optional[int] = None
    name: str
