from pydantic import BaseModel
from typing import Optional

class WeatherEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'une entrée météorologique.

    Attributes:
        id_city (Optional[int]): L'identifiant de la ville (facultatif).
        date (str): La date de l'entrée au format 'YYYY-MM-DD'.
        tmin (float): La température minimale en degrés Fahrenheit.
        tmax (float): La température maximale en degrés Fahrenheit.
        prcp (float): Les précipitations en pouces.
        snow (float): L'accumulation de neige en pouces.
        snwd (float): L'épaisseur de neige au sol en pouces.
        awnd (float): La vitesse moyenne du vent en miles par heure.
    """
    id_city: Optional[int] = None
    date: str
    tmin: float
    tmax: float
    prcp: float
    snow: float
    snwd: float
    awnd: float
