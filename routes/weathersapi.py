import json
import random

# 1. Ouvrez et chargez le fichier JSON
with open('../rdu-weather-history.json', 'r') as file:
    data = json.load(file)

# 2. Pour chaque élément, ajoutez un id, puis réorganisez les clés
for index, item in enumerate(data):
    item["id"] = index + 1  # Génération d'un identifiant unique
    item["id_city"] = random.randint(0, 6)

    # Réorganisation des clés
    keys_order = ['id', 'id_city'] + [key for key in item if key not in ['id', 'id_city']]
    data[index] = {key: item[key] for key in keys_order}

# 3. Sauvegardez le fichier JSON modifié
with open('rdu-weather-history.json', 'w') as file:
    json.dump(data, file, indent=4)
