from ghost import Ghost
from time import sleep

with ghost.start as session:
    page, extra_resources = session.open('https://www.redfin.com/city/18607/AZ/Tempe')
    session.click('#downloadLink', expect_loading=True)
    print (page.http_status)
    print (page.content)
    sleep(5)  # wait for the zip file to be downloaded
    print (session.http_resources)
