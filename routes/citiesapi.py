import json

# Existing city data
cities = [
    {"id": 1, "idcountries": 1, "name": "Paris"},
    {"id": 2, "idcountries": 2, "name": "New York"},
    {"id": 3, "idcountries": 1, "name": "Marseille"},
    {"id": 4, "idcountries": 3, "name": "Toronto"},
    {"id": 5, "idcountries": 1, "name": "Lyon"},
    {"id": 6, "idcountries": 2, "name": "Los Angeles"},
    {"id": 7, "idcountries": 3, "name": "Vancouver"}
]

# Save the updated data to a JSON file
with open('cities.json', 'w') as file:
    json.dump(cities, file, indent=4)

print("Three more cities added to 'cities.json'.")
