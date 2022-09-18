#from ast import Return
#from tkinter import E
from selenium_respectful import RespectfulWebdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import sys



#gameNo = 1
#date = "04/09/2022"
#MB = ("Thalia, Guardian of Thraben", "Archon of Emeria")
#SB = ("Mindbreak Trap", "Leyline of The Void")
#format = "Vintage"


class DriverController():
    def __init__(self):
        #adds options to the webdriver, in this case, to let webpage load, and bypass rate limiting
        driverOptions = webdriver.ChromeOptions()
        driverOptions.add_argument('--ignore-certificate-errors')
        driverOptions.add_argument('--ignore-ssl-errors')
        driverOptions.add_argument('--start-maximized')
        driverOptions.headless = True
        #driverOptions.add_argument('--disable-extensions')

        #downloads and runs a webdriver, that stops and is uninstalled after the program exits, using the options declared above
        chrome_path = ChromeDriverManager().install()
        chrome_service = Service(chrome_path)
        self.driver = webdriver.Chrome(options=driverOptions, service=chrome_service)



    def getSite(self, url):
        #gets the url passed through
        self.driver.get(url)


    def inputFormData(self, gameNo, format, MainB, SideB, date):
        #finds the format <select> tag, and selects the format passed in
        select_element = self.driver.find_element(By.XPATH, '//body/div/div/table/tbody/tr/td[1]/form/table/tbody/tr[4]/td[2]/select')
        select_object = Select(select_element)
        select_object.select_by_visible_text(format)

        '''each match is a best of three, and in games 2 to 3 more cards can be added (SB)
        so if it's not game 1, then SB is added to the cards, and the SB option is checked on the website'''
        if gameNo > 1:
            cards = MainB
        else:
            self.driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()
            cards = MainB + SideB
        
        #loops through the list of cards, writing each card into the <textarea>
        textarea = self.driver.find_element(By.XPATH, '//textarea[@name="cards"]')
        for listCard in range(0, len(cards)-1):
            textarea.send_keys(cards[listCard])
            textarea.send_keys(Keys.RETURN)

        #sets the 'date end' to the date of the match, so that deck possibilites from after that game aren't considered (as they don't exist at the time of playing)
        dateTo = self.driver.find_element(By.XPATH, '//input[@name="date_end"]')
        dateTo.send_keys(date)

        #clicks the submit button of the form
        dateTo = self.driver.find_element(By.XPATH, '//td[@colspan="2"]//input[@type="submit"]').click()


    def getRecord(self, deckName):
        decklist = []
        
        self.driver.implicitly_wait(1)
        try:
            WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH, '//body/div/div/div[7]/div[2]/div[3]/div[1]/div[2]/span'))
        except Exception as EX:
            print(EX)
            self.driver.quit()

        #finds each card, and adds it to the deckList list
        cards = self.driver.find_elements(By.XPATH, '//span[@class="L14"]')
        for card in cards:
            card = card.text
            decklist.append(card)
            #saves info to deckSave.db

        #selects the most populous deckName
        print(decklist)
        print(deckName)


    def cookieBanner(self):
        #clicks cookie banner, as it obstructs webdriver's view
        self.driver.find_element(By.XPATH, '//*[@id="cookie_window"]/div[2]/button').click()


    def getDeckUrls(self):
        deckUrls = []
        deckNames = []

        #loops through all decks on the page and gets the url to them and their name
        for decks in range(2, 27):
            url = self.driver.find_element(By.XPATH, f'//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{decks}]/td[2]/a')
            deckNames.append(url.text)
            deckUrls.append(url.get_attribute('href'))

        print(deckNames)
        return deckUrls, deckNames


    def quit(self):
        #stops the driver
        self.driver.quit()


if __name__ == "__main__":
    pass
else:
    #sets the base url
    url = "https://mtgtop8.com/search"

    #sets dc to an abbreviation of the class, so 'DriverController()' doesn't have to be infront of each object
    dc = DriverController()

    #calls the 'getSite()' object to set the url of the driver
    dc.getSite(url)

    #calls the 'cookieBanner()' object to clear the cookie banner
    dc.cookieBanner()

    #calls the 'inputFormData()' object to get all decks to be scraped
    dc.inputFormData(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    #gets the deck urls and names from the 'getDeckUrls()' object
    deckUrls, deckNames = dc.getDeckUrls()

    #loops through numbers 2 to 25, to get the relevant url for each deck, and then get each card from said deck
    for currentDeck in range(0,25):
        dc.getSite(deckUrls[currentDeck])
        dc.getRecord(deckNames[currentDeck])
    
    #calls the quit() object to stop the driver
    dc.quit()
