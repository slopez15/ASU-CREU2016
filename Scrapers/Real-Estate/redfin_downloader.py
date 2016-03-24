import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

download_path = os.getcwd() + "\\csv_data\\"
fp = webdriver.FirefoxProfile("C:/Users/crdia/AppData/Local/Mozilla/Firefox/Profiles/jy1aey5h.selenium")
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", download_path)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv");

browser = webdriver.Firefox(firefox_profile=fp)
browser.get("https://www.redfin.com")

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)
def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

def append_to_fault_file(newCity): #reference: http://pymotw.com/2/csv/
    print("appending to fault")
    os.chdir(download_path)
    fd = open('_fault_file.csv','a')
    fd.write('%s, %s\n' % newCity)
    fd.close()

def append_to_success_file(newCity): #reference: http://pymotw.com/2/csv/
    print("appending to success")
    os.chdir(download_path)
    fd = open('_success.csv','a')
    fd.write('%s, %s\n' % newCity)
    fd.close()

def already_faulty(current_city): #reference: http://pymotw.com/2/csv/
    match = False
    with open('_fault_file.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            success_cityState = ','.join(row)
            current_cityState = '%s, %s' % current_city
            if current_cityState == success_cityState:
                match = True
    return match

def already_obtained(current_city): #reference: http://pymotw.com/2/csv/
    os.chdir(download_path)
    match = False
    with open('_success.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            success_cityState = ','.join(row)
            current_cityState = '%s, %s' % current_city
            if current_cityState == success_cityState:
                match = True
    return match

def rename_file(docName):
    cityState = (docName[2], docName[0])
    os.chdir(download_path)
    files = filter(os.path.isfile, os.listdir(download_path))
    files = [os.path.join(download_path, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    newest_file = files[-1]
    if "redfin" in newest_file:
        newFilename = '%s, %s' % cityState
        os.rename(newest_file, newFilename+".csv")
        append_to_success_file(cityState)
    else:
        append_to_fault_file(cityState)

def collect_csv_data():
    with open('cities.csv', "r") as f:
        data = csv.reader(f)

        for row in data:
            cityState = (row[2], row[0])
            keys = '%s, %s' % cityState

            if row[0] != 'AR':  # Filter script by state
                print('Not AR')
            elif already_obtained(cityState):
                print(keys +': Already Obtained')
            elif already_faulty(cityState):
                print(keys +': Already Faulty')
            else:
                browser.implicitly_wait(10)
                browser.get("https://www.redfin.com")
                elem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input-box")))

                elem.clear()
                elem.send_keys(keys)
                try:
                    with wait_for_page_load(browser):
                        browser.find_element_by_class_name("search-input-box").submit()
                except:
                    pass
                # Check for an unrecognized city
                if browser.current_url == 'https://www.redfin.com/':
                    print('No listings for '+ keys)
                    append_to_fault_file(cityState)
                else:
                    # find download link. Throw excepion for a city with no listings
                    try:
                        elem = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "downloadLink"))).click()
                        rename_file(row)
                    except NoSuchElementException:
                        print('Empty Page for '+ keys)
                        append_to_fault_file(cityState)

collect_csv_data()
