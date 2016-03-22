import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

download_path = os.getcwd() + "\\csv_data\\"
fp = webdriver.FirefoxProfile("C:/Users/Chris/AppData/Roaming/Mozilla/Firefox/Profiles/lezp5kwl.selenium")
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", download_path)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv");

browser = webdriver.Firefox(firefox_profile=fp)
browser.get("https://www.redfin.com")

def append_to_fault_file(newCity): #reference: http://pymotw.com/2/csv/
    fd = open('fault_file.csv','a')
    fd.write('%s, %s\n' % newCity)
    fd.close()

def rename_file(docName):
    os.chdir(download_path)
    files = filter(os.path.isfile, os.listdir(download_path))
    files = [os.path.join(download_path, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    newest_file = files[-1]
    if "redfin" in newest_file:
        newFilename = '%s, %s' % cityState
        os.rename(newest_file, newFilename+".csv")
    else:
        append_to_fault_file('%s, %s' % cityState)

def collect_csv_data():
    with open('cities.csv', "r") as f:
        data = csv.reader(f)

        for row in data:
            if row[0] != 'AL':  # Filter script by state
                print('Not AL')
            
            else:
                elem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input-box")))
                cityState = (row[2], row[0])
                keys = '%s, %s' % cityState
                elem.clear()
                elem.send_keys(keys)
                elem.submit()
                browser.implicitly_wait(10)

                # Check for an unrecognized city
                if browser.current_url == 'https://www.redfin.com/':
                    print('No listings for '+ keys)
                    append_to_fault_file(cityState)
                else:
                    # find download link. Throw excepion for a city with no listings
                    try:
                        elem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "downloadLink")))
                        elem.click()
                        rename_file(cityState)
                    except NoSuchElementException:
                        print('Empty Page for '+ keys)
                        append_to_fault_file(cityState)

                browser.implicitly_wait(10)
                browser.get("https://www.redfin.com")

collect_csv_data()
