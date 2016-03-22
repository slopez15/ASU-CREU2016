import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

fp = webdriver.FirefoxProfile("C:/Users/Chris/AppData/Roaming/Mozilla/Firefox/Profiles/lezp5kwl.selenium")
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv");

browser = webdriver.Firefox(firefox_profile=fp)
browser.get("https://www.redfin.com")

fault_list = []

def rename_file(docName):
    os.chdir("C:/Users/Chris/Downloads/")
    files = filter(os.path.isfile, os.listdir("C:/Users/Chris/Downloads/"))
    files = [os.path.join("C:/Users/Chris/Downloads/", f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    newest_file = files[-1]
    if "redfin" in newest_file:
        os.rename(newest_file, docName+".csv")
    else:
        fault_list.append(docName)

with open('cities.csv', "r") as f:
    data = csv.reader(f)

    for row in data:
        if row[0] != 'AL':  # Filter script by state
            print('Not AL')
        else:
            elem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input-box")))
            keys = row[2] + ', ' + row[0]

            elem.clear()
            elem.send_keys(keys)
            elem.submit()
            browser.implicitly_wait(10)

            # Check for an unrecognized city
            if browser.current_url == 'https://www.redfin.com/':
                print('No listings for '+ keys)
                fault_list.append(keys)
            else:
                # find download link. Throw excepion for a city with no listings
                try:
                    elem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "downloadLink")))
                    elem.click()
                    rename_file(row[2] + '_' + row[0])
                except NoSuchElementException:
                    print('Empty Page for '+ keys)
                    fault_list.append(keys)

            browser.implicitly_wait(10)
            browser.get("https://www.redfin.com")
