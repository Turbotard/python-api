import json

# Charger les données depuis le fichier JSON
with open('rdu-weather-history.json', 'r') as file:
    data = json.load(file)