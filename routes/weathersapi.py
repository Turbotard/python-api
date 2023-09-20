import json
import random

with open('../rdu-weather-history.json', 'r') as file:
    data = json.load(file)
i = 1
for item in data:
    item["id"] = i
    item["idcities"] = random.randint(0, 6)
    i += 1


with open('rdu-weather-history.json', 'w') as file:
    json.dump(data, file, indent=4)
