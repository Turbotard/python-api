from pydantic import BaseModel
from typing import Optional

class PartialWeatherEntry(BaseModel):
    """
    Modèle Pydantic pour les mises à jour partielles d'une entrée météorologique.

    Attributes:
        tmin (Optional[float]): La température minimale en degrés Fahrenheit.
        tmax (Optional[float]): La température maximale en degrés Fahrenheit.
        prcp (Optional[float]): Les précipitations en pouces.
        snow (Optional[float]): L'accumulation de neige en pouces.
        snwd (Optional[float]): L'épaisseur de neige au sol en pouces.
        awnd (Optional[float]): La vitesse moyenne du vent en miles par heure.
    """
    id_city: Optional[int] = None
    date: Optional[str] = None
    tmin: Optional[float] = None
    tmax: Optional[float] = None
    prcp: Optional[float] = None
    snow: Optional[float] = None
    snwd: Optional[float] = None
    awnd: Optional[float] = None
