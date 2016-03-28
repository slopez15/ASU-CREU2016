'''START urllib '''
from urllib import request
import urllib
from ghost import Ghost

#simple request
#http://spotcrime.com
base = 'http://spotcrime.com'
url = 'http://spotcrime.com/al'
response = request.urlopen(url)
html = response.read()#bytes
#htmlString = html.decode("utf-8")#str



'''START BeautifulSoup '''
#type() - use to know types
from bs4 import BeautifulSoup
code = BeautifulSoup(html, "html.parser")
soup = code

#parse input [arrays]
#t = soup.find_all('table', class_="table table-condensed table-striped table-hover text-left")#bs4.element.ResultSet
#t = soup.find('table').find('tr').find('td').a['href']
#t = soup.find_all('table')
#t = t[1] #is array can't findAll unless is soup

#find_all methods
#soup = BeautifulSoup((str)(t), "html.parser")
#t = soup.find_all('tr')
#soup.findAll('tag', { "class" : "" })
#soup.find_all('tag', class_="")
#<table class="table table-condensed table-striped table-hover text-left">




'''
i want to find all table, then find all tr childeren,
then all td children, then a children in href to check if /state/

#prefer not to use data struct (memory waste), or multiple loops
...

#could find one, go inside, then get next_sibling (same) until none
prob:every other is empty, might be a structure thing.

#.nextSibling way; last sibling 'None'-cant lower for compare or mess up,

#can findAll then make soup again then findall
'''



###FIND ALL WAY (prob: brackets, memory, speed (if looping))
tableCount = 0
tdCount = 0
td2and3Count = 0
aCount = 0

t1_hrefs = []
hrefs = [] #onlyhrefs we care about
tables2and3 = []

tables = soup.findAll('table') #allow soup methods / bs4.element.ResultSet #assume there are 3 tables on all state pages
tableCount = len(tables) # should be 3
#print((str)(t[2]))
#soupTables = (BeautifulSoup((str)(tables), "html.parser")) #list type


#get table 1 href info 'crimeMap,Stats,LocalReports,Alerts'	#\xa0 <- utf8 -> \xc2\xa0
tdTags = (BeautifulSoup((str)(tables[0]), "html.parser")).findAll('td')
for tdTag in tdTags:
	if ( tdTag.get_text() != '\xa0'): #assumes if there's text, there's a link
		t1_hrefs.append(tdTag.find('a').get('href')) #!!!*** .get is better than .find or 'a[href]', returns str instead of NoneType
	tdCount += 1 #/al/ =20, 'a'Tags=21
hrefs [:] = t1_hrefs [:] #collect wanted table1 hrefs

#table 2 hrefs | 'MoreAreas' & 'AdditionalStateCrimeResourcesAndLinks'
tables2and3 [:] = tables [:]
del tables2and3[0] #remove table1
del tables2and3[1]
hrefAttribs = (BeautifulSoup((str)(tables2and3), "html.parser")).findAll('a')
for hrefAttrib in hrefAttribs:
	hrefs.append(hrefAttrib.get('href')) #collect wanted table1&2 hrefs
	td2and3Count += 1

#use Ghost to get Dynamic HTML = crimeData




##'''
#print
#test type & inside
i=0
while(i < len(hrefs)):
	print(hrefs[i])
	#print(type(hrefs[i]))
	i += 1
print ("hello")
print ("tables: ", tableCount)
print ("td's in table1: ", tdCount)
print ("hrefs in table1: ", len(t1_hrefs))
print ("tds in table2&3: ", td2and3Count)
print ("hrefs overall: ", len(hrefs))

#'''


##### STATE ACRONYMS####
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


##### Ending #####
#optimize by 'del var' when done with var in prgm?
#ending the program
#response.close()
