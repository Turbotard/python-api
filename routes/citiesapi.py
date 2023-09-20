import json

# Existing city data
cities = [
    {"id": 1, "id_country": 1, "name": "Paris"},
    {"id": 2, "id_country": 2, "name": "New York"},
    {"id": 3, "id_country": 1, "name": "Marseille"},
    {"id": 4, "id_country": 3, "name": "Toronto"},
    {"id": 5, "id_country": 1, "name": "Lyon"},
    {"id": 6, "id_country": 2, "name": "Los Angeles"},
    {"id": 7, "id_country": 3, "name": "Vancouver"}
]

# Save the updated data to a JSON file
with open('cities.json', 'w') as file:
    json.dump(cities, file, indent=4)

print("Three more cities added to 'cities.json'.")
