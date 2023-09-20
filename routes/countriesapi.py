import json

# Example country data with ID and name
countries = [
    {"id": 1, "name": "France"},
    {"id": 2, "name": "United States"},
    {"id": 3, "name": "Canada"},
    # Add more countries here with unique IDs and names
]

# Save the data to a JSON file
with open('countries.json', 'w') as file:
    json.dump(countries, file, indent=4)

print("JSON file 'countries.json' successfully created, containing only IDs and names of countries.")
