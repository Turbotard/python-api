from pydantic import BaseModel
from typing import Optional

class PartialWeatherEntry(BaseModel):
    """
    Modèle Pydantic pour les mises à jour partielles d'une entrée météorologique.

    Attributes:
        id_city (Optional[int]): L'identifiant de la ville (facultatif).
        date (Optional[str]): La date de l'entrée au format 'YYYY-MM-DD' (facultatif).
        tmin (Optional[float]): La température minimale en degrés Fahrenheit (facultatif).
        tmax (Optional[float]): La température maximale en degrés Fahrenheit (facultatif).
        prcp (Optional[float]): Les précipitations en pouces (facultatif).
        snow (Optional[float]): L'accumulation de neige en pouces (facultatif).
        snwd (Optional[float]): L'épaisseur de neige au sol en pouces (facultatif).
        awnd (Optional[float]): La vitesse moyenne du vent en miles par heure (facultatif).
    """
    id_city: Optional[int] = None
    date: Optional[str] = None
    tmin: Optional[float] = None
    tmax: Optional[float] = None
    prcp: Optional[float] = None
    snow: Optional[float] = None
    snwd: Optional[float] = None
    awnd: Optional[float] = None
