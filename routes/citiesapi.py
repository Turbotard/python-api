import json

# Existing city data
cities = [
    {"id": 1, "idcountries": 1, "name": "Paris"},
    {"id": 2, "idcountries": 2, "name": "New York"},
    {"id": 3, "idcountries": 1, "name": "Marseille"},
    {"id": 4, "idcountries": 3, "name": "Toronto"},
    # Add three more cities
    {"id": 5, "idcountries": 2, "name": "Los Angeles"},
    {"id": 6, "idcountries": 4, "name": "Berlin"},
    {"id": 7, "idcountries": 5, "name": "Sydney"},
]

# Save the updated data to a JSON file
with open('cities.json', 'w') as file:
    json.dump(cities, file, indent=4)

print("Three more cities added to 'cities.json'.")
