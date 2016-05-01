import csv
import json
import requests

with open('stadiums.csv', "r") as f:
    data = csv.reader(f)
    to_json = []
    missing = []

    base_addr = "https://maps.googleapis.com/maps/api/geocode/json?address="

    for row in data:
        r = requests.get(base_addr+row[0])
        geocoder_result = r.json()
        if len(geocoder_result["results"]) > 0:
            to_json.append( {
                              "@context": "https://raw.githubusercontent.com/slopez15/ASU-CREU2016/master/JSON-Data/stadiums_context.jsonld",
                              "@type" : "https://schema.org/StadiumOrArena",
                              "name" : row[0],
                              "capacity" : row[1],
                              "address" : geocoder_result["results"][0]["formatted_address"],
                              "geo": {
                                  "@type": "GeoCoordinates",
                                  "latitude" : geocoder_result["results"][0]["geometry"]["location"]["lat"],
                                  "longitude" : geocoder_result["results"][0]["geometry"]["location"]["lng"],
                              },
                              "foundingDate" : row[4],
                              "teams" : row[6],
                              "brand" : row[5]
                            })
        else:
            missing.append(row)
        with open("stadiums.json", "w") as outfile:
           json.dump(to_json, outfile, indent=4)
        with open("missing.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(missing)
