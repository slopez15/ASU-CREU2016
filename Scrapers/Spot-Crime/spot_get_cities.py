#reference: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
import requests
import csv

def write_to_csv(data,file_name): #reference: http://pymotw.com/2/csv/
  with open(file_name,'w') as f: #existing file with the same name will be overwritten
    writer = csv.writer(f, lineterminator='\n')
    for i in range(len(data)):
      if data[i]:
        writer.writerow([data[i]])#while the square brackets around data[i] might seem unnecessary, they are required
                                  #for desired output. More details here  http://stackoverflow.com/a/27065792

def get_city_urls():
  #the base urls for scraping - the school list is paginated
  with open("spot_states.txt") as f:
    base_urls = f.read().splitlines()

  #create a list individual school district urls
  for url in base_urls:
    with open("spot_area_urls.txt") as f:
      states = f.read().splitlines()
    r = requests.get(url)
    data=r.text
    soup = BeautifulSoup(data, "html.parser")

    main_table = soup.findall(class_="table table-condensed table-striped table-hover text-left")


    for cur_link in all_links:
      cur_url = cur_link.get('href')
      for i in range(0, 50):
          print(states[i])
          length = len(states[i])
          if cur_url[0:length] == states[i] and len(cur_url)>length:
              school_district_urls.append(url_pre+cur_url+url_post)
              break

  write_to_csv(school_district_urls,"school_district_urls2.csv")


get_school_urls()
