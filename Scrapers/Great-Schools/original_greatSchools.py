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

def get_school_urls():
  #the base url to start scraping - the school list is paginated
  base_urls = ["http://www.greatschools.org/schools/districts/Wisconsin/WI","http://www.greatschools.org/schools/districts/Wisconsin/WI/2"]
  school_district_urls = []
  url_pre = "http://www.greatschools.org"
  url_post = "schools/"

  #create a list individual school district urls
  for url in base_urls:
    r = requests.get(url)
    data=r.text
    soup = BeautifulSoup(data, "html.parser")
    all_links = soup.find_all('a')#get all links on page
    for cur_link in all_links:
      cur_url = cur_link.get('href')
      if cur_url[0:11] == "/wisconsin/" and len(cur_url)>11:
        school_district_urls.append(url_pre+cur_url+url_post)

  write_to_csv(school_district_urls,"school_district_urls.csv")

def get_school_info(file_name):
  school_district_urls = []
  with open(file_name,'r') as f:
    reader = csv.reader(f)
    for row in reader:
      school_district_urls.append(row[0])

  school_data=[]
  for cur_url in school_district_urls:
    print(cur_url)
    r = requests.get(cur_url)
    data = r.text
    soup = BeautifulSoup(data)
    try:
      district_name = soup.find_all('input',id="js-schoolResultsSearch")[0].get('value')
      school_names = soup.find_all('a',class_="open-sans_sb mbs font-size-medium rs-schoolName")
      school_addresses = soup.find_all(class_="hidden-xs font-size-small rs-schoolAddress")
      school_ratings = soup.find_all(class_="gs-rating-sm average ma") #data is two siblings in
      school_review_count = soup.find_all(class_="font-size-small js-reviewCount")

      for i in range(len(school_names)):
        school_data.append([district_name,school_names[i].text,school_addresses[i].text])
      print(district_name + " done")
    except:
      pass
  write_to_csv(school_data,"school_data.csv")

get_school_urls()
get_school_info("school_district_urls.csv")
