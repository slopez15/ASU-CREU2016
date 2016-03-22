import csv
import json
import requests

with open('city_state.csv', "r") as f:
    data = csv.reader(f)
    to_json = []

    for row in data:
        r = requests.get(base_addr+row[0])
        geocoder_result = r.json()
        to_json.append( {
                          "Stadium" : row[0],
                          "Capacity"   : row[1],
                          "Location" : geocoder_result,
                          "Year opened" : row[3],
                          "Type" : row[4],
                          "Tenant" : row[5]
                        })
        with open("stadiums.json", "w") as outfile:
           json.dump(to_json, outfile, indent=4)
