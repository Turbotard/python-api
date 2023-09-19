from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Charger les données depuis le fichier JSON
with open('rdu-weather-history.json', 'r') as file:
    data = json.load(file)

# Initialisation du compteur de requêtes pour chaque route
request_counts = {
    'root': 0,
    'get_all_data': 0,
    'filter_by_date': 0,
    'filter_by_precipitation': 0,
    'filter_by_temperature': 0,
    'add_entry': 0,
    'delete_entry': 0,
    'update_entry': 0,
}
from datetime import datetime

from fastapi import FastAPI
import json

with open('rdu-weather-history.json') as test:
    data = json.load(test)
print(data)

app = FastAPI()


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
        dict: Un message de salutation avec le nombre de requêtes traitées.
    """
    request_counts['root'] += 1
    return {"request_count": request_counts['root'], "message": "Bienvenue dans l'API de données météorologiques."}


@app.get("/data")
def get_all_data():
    """
    Route pour consulter toutes les données météorologiques.

    Returns:
        dict: Le nombre de requêtes traitées et une liste de toutes les entrées de données.
    """
    request_counts['get_all_data'] += 1
    return {"request_count": request_counts['get_all_data'], "data": data}


@app.get("/data/filter-by-date")
def filter_by_date(start_date: str, end_date: str, order: str = "asc"):
    """
    Route pour filtrer les données par plage de dates.

    Args:
        start_date (str): La date de début au format 'YYYY-MM-DD'.
        end_date (str): La date de fin au format 'YYYY-MM-DD'.

    Returns:
        dict: Le nombre de requêtes traitées et une liste d'entrées de données comprises entre les dates spécifiées.
    """
    request_counts['filter_by_date'] += 1
    filtered_data = [entry for entry in data if start_date <= entry['date'] <= end_date]
    sorted_data = sorted(filtered_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
                         reverse=(order == "desc"))

    return {"request_count": request_counts['filter_by_date'], "filtered_data": sorted_data}


@app.get("/data/filter-by-precipitation")
def filter_by_precipitation(min_prcp: Optional[float] = None, max_prcp: Optional[float] = None, order: str = "asc"):
    """
    Route pour filtrer les données par plage de précipitations.

    Args:
        min_prcp (float, optional): La valeur minimale des précipitations en pouces.
        max_prcp (float, optional): La valeur maximale des précipitations en pouces.
        order (string): trie la valeure soit asc pour croissant soit desc pour décroissant
    Returns:
        dict: Le nombre de requêtes traitées et une liste d'entrées de données filtrées en fonction des précipitations spécifiées.
    """
    request_counts['filter_by_precipitation'] += 1
    if min_prcp is None and max_prcp is None:
        return {"request_count": request_counts['filter_by_precipitation'], "data": data}

    filtered_data = []

    for entry in data:
        prcp = entry.get('prcp')
        if prcp is not None and (min_prcp is None or prcp >= min_prcp) and (max_prcp is None or prcp <= max_prcp):
            filtered_data.append(entry)
    sorted_data = sorted(filtered_data, key=lambda x: x["prcp"], reverse=(order == "desc"))
    return {"request_count": request_counts['filter_by_precipitation'], "filtered_data": sorted_data}


@app.get("/data/filter-by-temperature")
def filter_by_precipitation(temp: float, order: str = "asc"):
    """
    Route pour filtrer les données par température trié par rapport au min

    Args:
        temp: (float) Temparature
        order (string): trie la valeure soit asc pour croissant soit desc pour décroissant

    Returns:
        dict : les températurs filtrés entre tmin et tmax
    """
    request_counts['filter_by_temperature'] += 1
    filtered_data = []
    for entry in data:
        tmin = entry.get('tmin')
        tmax = entry.get('tmax')
        if temp >= tmin and temp <= tmax:
            filtered_data.append(entry)
    sorted_data = sorted(filtered_data, key=lambda x: x["tmin"], reverse=(order == "desc"))
    return {"request_count": request_counts['filter_by_temperature'], "filtered_data": sorted_data}


@app.post("/data/add-entry")
def add_entry(new_entry: WeatherEntry):
    """
    Route pour ajouter une nouvelle entrée de données.

    Args:
        new_entry (WeatherEntry): Les données de la nouvelle entrée.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    request_counts['add_entry'] += 1
    data.append(new_entry.dict())
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"request_count": request_counts['add_entry'], "message": "Nouvelle entrée ajoutée avec succès!"}


@app.delete("/data/delete-entry")
def delete_entry(date_to_delete: str):
    """
    Route pour supprimer une entrée de données par date.

    Args:
        date_to_delete (str): La date de l'entrée à supprimer au format 'YYYY-MM-DD'.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    request_counts['delete_entry'] += 1
    data[:] = [entry for entry in data if entry['date'] != date_to_delete]
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"request_count": request_counts['delete_entry'],
            "message": f"Entrée avec date {date_to_delete} supprimée avec succès!"}


@app.put("/data/update-entry")
def update_entry(updated_entry: WeatherEntry):
    """
    Route pour mettre à jour une entrée de données par date.

    Args:
        updated_entry (WeatherEntry): Les données mises à jour de l'entrée.

    Returns:
        dict: Le nombre de requêtes traitées et un message de confirmation.
    """
    request_counts['update_entry'] += 1
    date_to_update = updated_entry.date
    data[:] = [entry if entry['date'] != date_to_update else updated_entry.dict() for entry in data]
    with open('rdu-weather-history.json', 'w') as file:
        json.dump(data, file, indent=4)
    return {"request_count": request_counts['update_entry'],
            "message": f"Entrée avec date {date_to_update} mise à jour avec succès!"}


@app.get("/data/statistics")
def stats():
    """
    Route qui affiche le nombres de requètes faites pour chaques route

    Returns:
        request_count : renvoie des counters des utilisations de chaques routes

    """
    return {"request_count_root": request_counts['root'],
            "request_count_all_data": request_counts['get_all_data'],
            "request_count_filter_by_date": request_counts['filter_by_date'],
            "request_count_filter_by_precipitation": request_counts['filter_by_precipitation'],
            "request_count_filter_by_temperature": request_counts['filter_by_temperature'],
            "request_count_add_entry": request_counts['add_entry'],
            "request_count_delete_entry": request_counts['delete_entry'],
            "request_count_update_entry": request_counts['update_entry']}
