from fastapi import FastAPI
import json

with open('rdu-weather-history.json') as test :
     data = json.load(test)
print(data)
