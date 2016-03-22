#reference: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import requests
import csv
import json


def read_addresses():
    base_addr = "https://maps.googleapis.com/maps/api/geocode/json?address="
    to_json = []
    with open('all_school_data.csv', "r") as f:
        data = csv.reader(f)
        for row in data:
          content = ','.join(row)
          content = str(content)[2:-2].split("', '")
          print(content)
          r = requests.get(base_addr+content[2])
          geocoder_result = r.json()
          to_json.append( {
                            "District" : content[0],
                            "School"   : content[1],
                            "Location" : geocoder_result
                          })
    with open("schools.json", "w") as outfile:
       json.dump(to_json, outfile, indent=4)

read_addresses()
