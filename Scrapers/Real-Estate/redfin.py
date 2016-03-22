from ghost import Ghost

ghost = Ghost()
#page, resources = ghost.open('https://www.redfin.com/')
page, resources = ghost.open('https://www.redfin.com/city/18607/AZ/Tempe')
ghost.click('#downloadLink')
