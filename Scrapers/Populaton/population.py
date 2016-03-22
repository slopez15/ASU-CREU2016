import csv
import json
import requests

with open('city_state.csv', "r") as f:
    data = csv.reader(f)
    to_json = []

    for row in data:
        to_json.append( {
                          "City" : row[0],
                          "State"   : row[1],
                          "Population" : row[2],
                        })
        with open("city_state_population.json", "w") as outfile:
           json.dump(to_json, outfile, indent=4)
