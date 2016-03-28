#!/usr/bin/env PY34_HOME
#C:\Python34\

import sys
import time
print (sys.version)
#time.sleep(1)


'''START urllib '''
from urllib import request
import urllib

#simple request
#http://spotcrime.com
base = 'http://spotcrime.com'
url = 'http://spotcrime.com/al/auburn'
response = request.urlopen(url)
html = response.read()#bytes
#htmlString = html.decode("utf-8")#str



'''START BeautifulSoup '''
#type() - use to know types
from bs4 import BeautifulSoup
code = BeautifulSoup(html, "html.parser")
soup = code

code = code.find("table_container")

#print (code)


'''START Ghost.py '''
from ghost import Ghost
ghost = Ghost() #Ghost web client instance
session = ghost.start()
page, resources = session.open(url) #open web page #see 'Open a Webpage' http://jeanphix.me/Ghost.py/#intro
#print(type(page))  #ghost.ghost.HttpResource
#print(type(resources)) #list

print("\nwaitingForButton...")
time.sleep(1)
session.wait_for_selector('#SignupModal .modal-header:first-child button')
print("\nClick button...")
session.click('#SignupModal .modal-header:first-child button')#leftClick on close button

#tupleElem = session.region_for_selector('#SignupModal .modal-header:first-child button')
result, resources = session.evaluate("document.getElementById('table_container')") #execute javascript aka js #code just like chrome console <probibly not related>

#SessionString = str(session.content('#SignupModal .modal-header:first-child button'))
#print(str(result))
#tdTags = (BeautifulSoup((str)(), "html.parser")).findAll('td')

print("\nshowing...")
session.show()
print("\npause...")
time.sleep(5)
print("\nclosing...")
session.hide()
#sys.exit(0)
#exit()
#'''#
    #SOUP?
afterImage = session.content
#print("session.content type: ")
#print(type(afterImage)) #str
#afterImage = (request.urlopen(url)).read()
code = BeautifulSoup(afterImage, "html.parser")
#Obtain table_container with crime data
crimeTable = code.find(id = 'table_container')
code = BeautifulSoup((str)(crimeTable), "html.parser").find_all('a')
    #extract crime(<h4>), date(<p>class=list-group-item-text crime-date), address(<p>class=list-group-item-text crime-address)
    #'''#

crimeContent = []
dateContent = [] #onlyhrefs we care about
addressContent = []

#crimeContent = BeautifulSoup((str)(code), "html.parser").find_all('h4')
for aTag in code:
	if ( aTag.get_text() != '\xa0'):
		crimeContent.append(aTag.find('h4').get_text()) #!!!*** .get is better than .find or 'a[href]', returns str instead of NoneType
		
#dateContent = BeautifulSoup((str)(code), "html.parser").find_all(class="list-group-item-text crime-date")
for aTag in code:
	if ( aTag.get_text() != '\xa0'):
		dateContent.append(aTag.find('p').get_text()) #!!!*** .get is better than .find or 'a[href]', returns str instead of NoneType
		addressContent.append(aTag.find('p').next_sibling.get_text()) #!!!*** .get is better than .find or 'a[href]', returns str instead of NoneType
#addressContent = BeautifulSoup((str)(code), "html.parser").find_all(class="list-group-item-text crime-address") 
'''
for aTag in code:
	if ( aTag.get_text() != '\xa0'):
		addressContent.append(aTag.) #!!!*** .get is better than .find or 'a[href]', returns str instead of NoneType
'''



'''
tdTags = (BeautifulSoup((str)(tables[0]), "html.parser")).findAll('td')
for tdTag in tdTags:
	if ( tdTag.get_text() != '\xa0'): #assumes if there's text, there's a link
		t1_hrefs.append(tdTag.find('a').get('href')) #!!!*** .get is better than .find or 'a[href]', returns str instead of NoneType
	tdCount += 1 #/al/ =20, 'a'Tags=21
hrefs [:] = t1_hrefs [:] #collect wanted table1 hrefs
'''
#'''#
code = BeautifulSoup((str)(code), "html.parser")
crimeContent = BeautifulSoup((str)(crimeContent), "html.parser")
dateContent = BeautifulSoup((str)(dateContent), "html.parser")
addressContent = BeautifulSoup((str)(addressContent), "html.parser")

code = code.prettify()
crimeContent = crimeContent.prettify()
dateContent = dateContent.prettify()
addressContent = addressContent.prettify()


#'''
#------#Print-------
#print(code)
print(crimeContent)
print(dateContent)
print(addressContent)


















