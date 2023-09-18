from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import json

app = FastAPI()

# Charger les données depuis le fichier JSON
with open('rdu-weather-history.json', 'r') as file:
    data = json.load(file)


class WeatherEntry(BaseModel):
    """
    Modèle Pydantic pour la création et la mise à jour d'une entrée météorologique.

    Attributes:
        date (str): La date de l'entrée au format 'YYYY-MM-DD'.
        tmin (float): La température minimale en degrés Fahrenheit.
        tmax (float): La température maximale en degrés Fahrenheit.
        prcp (float): Les précipitations en pouces.
        snow (float): L'accumulation de neige en pouces.
        snwd (float): L'épaisseur de neige au sol en pouces.
        awnd (float): La vitesse moyenne du vent en miles par heure.
    """
    date: str
    tmin: float
    tmax: float
    prcp: float
    snow: float
    snwd: float
    awnd: float


@app.get("/")
def read_root():
    """
    Route d'accueil de l'API.

    Returns:
        dict: Un message de salutation.
    """
    return {"message": "Bienvenue dans l'API de données météorologiques."}


@app.get("/data")
def get_all_data():
    """
    Route pour consulter toutes les données météorologiques.

    Returns:
        list[dict]: Une liste de toutes les entrées de données.
    """
    return data


@app.get("/data/filter-by-date")
def filter_by_date(start_date: str, end_date: str):
    """
    Route pour filtrer les données par plage de dates.

    Args:
        start_date (str): La date de début au format 'YYYY-MM-DD'.
        end_date (str): La date de fin au format 'YYYY-MM-DD'.

    Returns:
        list[dict]: Une liste d'entrées de données comprises entre les dates spécifiées.
    """
    filtered_data = [entry for entry in data if start_date <= entry['date'] <= end_date]
    return filtered_data


@app.get("/data/filter-by-precipitation")
def filter_by_precipitation(min_prcp: Optional[float] = None, max_prcp: Optional[float] = None):
    """
    Route pour filtrer les données par plage de précipitations.

    Args:
        min_prcp (float, optional): La valeur minimale des précipitations en pouces.
        max_prcp (float, optional): La valeur maximale des précipitations en pouces.

    Returns:
        list[dict]: Une liste d'entrées de données filtrées en fonction des précipitations spécifiées.
    """
    if min_prcp is None and max_prcp is None:
        return data

    filtered_data = []

    for entry in data:
        prcp = entry.get('prcp')
        if prcp is not None and (min_prcp is None or prcp >= min_prcp) and (max_prcp is None or prcp <= max_prcp):
            filtered_data.append(entry)

    return filtered_data


@app.post("/data/add-entry")
def add_entry(new_entry: WeatherEntry):
    """
    Route pour ajouter une nouvelle entrée de données.

    Args:
        new_entry (WeatherEntry): Les données de la nouvelle entrée.

    Returns:
        dict: Un message de confirmation.
    """
    data.append(new_entry.dict())
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"message": "Nouvelle entrée ajoutée avec succès!"}


@app.delete("/data/delete-entry")
def delete_entry(date_to_delete: str):
    """
    Route pour supprimer une entrée de données par date.

    Args:
        date_to_delete (str): La date de l'entrée à supprimer au format 'YYYY-MM-DD'.

    Returns:
        dict: Un message de confirmation.
    """
    data[:] = [entry for entry in data if entry['date'] != date_to_delete]
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"message": f"Entrée avec date {date_to_delete} supprimée avec succès!"}


@app.put("/data/update-entry")
def update_entry(updated_entry: WeatherEntry):
    """
    Route pour mettre à jour une entrée de données par date.

    Args:
        updated_entry (WeatherEntry): Les données mises à jour de l'entrée.

    Returns:
        dict: Un message de confirmation.
    """
    date_to_update = updated_entry.date
    data[:] = [entry if entry['date'] != date_to_update else updated_entry.dict() for entry in data]
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"message": f"Entrée avec date {date_to_update} mise à jour avec succès!"}
