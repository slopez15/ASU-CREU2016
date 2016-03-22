#reference: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import requests
import csv

def write_to_csv(data,file_name): #reference: http://pymotw.com/2/csv/
  with open(file_name,'w') as f: #existing file with the same name will be overwritten
    writer = csv.writer(f, lineterminator='\n')
    for i in range(len(data)):
      if data[i]:
        writer.writerow([data[i]])

def get_school_urls():
  #the base urls for scraping - the school list is paginated
  with open("gc_districts_by_state_urls.txt") as f:
    base_urls = f.read().splitlines()

  school_district_urls = []
  url_pre = "http://www.greatschools.org"
  url_post = "schools/"

  #create a list individual school district urls
  for url in base_urls:
    with open("district_urls_state_path.txt") as f:
      states = f.read().splitlines()
    r = requests.get(url)
    data=r.json()
    soup = BeautifulSoup(data, "html.parser")
    all_links = soup.find_all('a') # get all links on page

    for cur_link in all_links:
      cur_url = cur_link.get('href')
      for i in range(0, 50):
          print(states[i])
          length = len(states[i])
          if cur_url[0:length] == states[i] and len(cur_url)>length:
              school_district_urls.append(url_pre+cur_url+url_post)
              break

  write_to_csv(school_district_urls,"school_district_urls.csv")


get_school_urls()
