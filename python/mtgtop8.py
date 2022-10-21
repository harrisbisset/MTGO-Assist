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


class DriverController():
    def __init__(self, gameNums, format, deckLists, date):
        
        #sets url
        url = "https://mtgtop8.com/search"

        #adds options to the webdriver, in this case, to let webpage load, and bypass rate limiting
        driverOptions = webdriver.ChromeOptions()
        driverOptions.add_argument('--ignore-certificate-errors')
        driverOptions.add_argument('--ignore-ssl-errors')
        driverOptions.add_argument('--start-maximized')
        driverOptions.headless = True
        driverOptions.add_argument('--disable-extensions')

        #downloads and runs a webdriver, that stops and is uninstalled after the program exits, using the options declared above
        chrome_path = ChromeDriverManager().install()
        chrome_service = Service(chrome_path)
        self.driver = webdriver.Chrome(options=driverOptions, service=chrome_service)


        for gameNum in range(0,gameNums):
            #calls the 'getSite()' object to set the url of the driver
            self.getSite(url)

            if gameNum == 0:
                #calls the 'cookieBanner()' object to clear the cookie banner
                self.cookieBanner()

            #calls the 'inputFormData()' object to get all decks to be scraped
            self.inputFormData(gameNum, format, deckLists, date)

            #gets the deck urls and names from the 'getDeckUrls()' object
            deckUrls, deckNames = self.getDeckUrls()

            #calls getDeckName() to create a dictionary of deckNames and %
            deckNames = self.getDeckNames(deckNames)

            #loops through numbers 2 to 25, to get the relevant url for each deck, and then get each card from said deck
            for currentDeck in range(0,25):
                self.getSite(deckUrls[currentDeck])
                self.getRecord(deckNames[currentDeck])
        

        #calls the quit() object to stop the driver
        self.quit()

        return deckNames



    def getSite(self, url):
        
        #gets the url passed through
        self.driver.get(url)



    def inputFormData(self, gameNum, format, deckLists, date):
        
        #format is currently not discerable from the logs, so this should always be true
        if format is not None:
            #finds the format <select> tag, and selects the format passed in
            select_element = self.driver.find_element(By.XPATH, '//body/div/div/table/tbody/tr/td[1]/form/table/tbody/tr[4]/td[2]/select')
            select_object = Select(select_element)
            select_object.select_by_visible_text(format)

        '''each match is a best of three, and in games 2 to 3 more cards can be added (SB)
        so if it's not game 1, then SB is added to the cards, and the SB option is checked on the website'''
        if gameNum > 0:
            self.driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()

        #includes cards found in games played so far, as the what cards were sideboarded or not is impossible to find out
        cards = deckLists[0:gameNum+1]

        #loops through the list of cards, writing each card into the <textarea>
        textarea = self.driver.find_element(By.XPATH, '//textarea[@name="cards"]')
       
       #writes the cards to the textbox
        for deck in cards:
            for listCard in deck:
                print(listCard)
                textarea.send_keys(listCard)
                textarea.send_keys(Keys.RETURN)

        #reformats the date
        x, y, z = date.split('/')
        date = z + '/' + y + '/' + x

        #sets the 'date end' to the date of the match, so that deck possibilites from after that game aren't considered (as they don't exist at the time of playing)
        dateTo = self.driver.find_element(By.XPATH, '//input[@name="date_end"]')
        dateTo.send_keys(date)

        #clicks the submit button of the form
        self.driver.find_element(By.XPATH, '//td[@colspan="2"]/input[@type="submit"]').click()



    def getRecord(self, deckName):
        decklist = []

        #finds each card, and adds it to the deckList list
        cards = self.driver.find_elements(By.XPATH, '//span[@class="L14"]')
        for card in cards:
            card = card.text
            decklist.append(card)
        
        #save info to deckSave.db



    def cookieBanner(self):
        
        #clicks cookie banner, as it obstructs webdriver's view
        self.driver.find_element(By.XPATH, '//*[@id="cookie_window"]/div[2]/button').click()



    def getDeckUrls(self):
        deckUrls = []
        deckNames = []
        
        #loops through all decks on the page and gets their and name
        for decks in range(2, 27):
            url = self.driver.find_element(By.XPATH, f'//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{decks}]/td[2]/a')
            deckNames.append(url.text)
            deckUrls.append(url.get_attribute('href'))

        return deckUrls, deckNames



    def quit(self):
        
        #stops the driver
        self.driver.quit()



    def getDeckNames(self, deckNames):
        
        #creates a dictionary of deckNames
        dictNames = {deckName:0 for deckName in deckNames}

        #gets number of decks with same name
        for deckName in deckNames:
            dictNames[deckName] = dictNames[deckName] + 1
        
        #gets percentage chance of said deck
        for deckName in dictNames:
            dictNames[deckName] = dictNames[deckName] / len(deckNames)

        return dictNames



if __name__ != "__main__":
    if sys.argv[1] == "":
        DriverController(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
