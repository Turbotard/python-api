import json
import random

with open('../rdu-weather-history.json', 'r') as file:
    data = json.load(file)

for item in data:
    item["idcities"] = random.randint(0, 6)

with open('rdu-weather-history.json', 'w') as file:
    json.dump(data, file, indent=4)
