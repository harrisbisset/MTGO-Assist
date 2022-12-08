from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import sys


class DriverController():
    def __init__(self, format, deckLists, date):
        self.format = format
        self.deckLists = deckLists
        self.date = date
    
    def startup(self):
        #sets url
        self.url = "https://mtgtop8.com/search"

        #adds options to the webdriver, in this case, to let webpage load, and bypass rate limiting
        driverOptions = webdriver.ChromeOptions()
        driverOptions.add_argument('--ignore-certificate-errors')
        driverOptions.add_argument('--ignore-ssl-errors')
        driverOptions.add_argument('--start-maximized')
        driverOptions.headless = True


        #check validity of comment
        #downloads and runs a webdriver, that stops and is uninstalled after the program exits, using the options declared above
        chrome_path = ChromeDriverManager().install()
        chrome_service = Service(chrome_path)
        self.driver = webdriver.Chrome(options=driverOptions, service=chrome_service)


    def returnDictNames(self):

        #calls the 'getSite()' method to open the url through the driver
        self.getSite()

        #calls the 'cookieBanner()' method to try and clear the cookie banner
        self.clearCookieBanner()

        #calls the 'inputFormData()' method to get all decks to be scraped
        self.inputFormData(self.format, self.refactorDecklist(), self.date)

        #gets the deck urls and names from the 'getDeckUrls()' method
        deckNames = self.getDeckNames()

        #if there are no decks found, then return deckNames (will have value of 'unknown')
        if deckNames == 'unknown':
            self.quit()
            return deckNames

        #calls getDeckName() to create a dictionary of deckNames and %
        dictNames = self.getDictNames(deckNames)

        #commented out, as driver doesn't need to be stopped until final
        #self.quit()

        print(dictNames)
        return dictNames



    def getSite(self):
        self.driver.get(self.url)



    def inputFormData(self, format, deckList, date):
        
        #format is currently not discerable from the logs, so this should always be true
        if format is not None:
            #finds the format <select> tag, and selects the format passed in
            selectElement = self.driver.find_element(By.XPATH, '//body/div/div/table/tbody/tr/td[1]/form/table/tbody/tr[4]/td[2]/select')
            selectObject = Select(selectElement)
            selectObject.select_by_visible_text(format)

        self.driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()

        #includes cards found in games played so far, as the what cards were sideboarded or not is impossible to find out

        #loops through the list of cards, writing each card into the <textarea>
        textarea = self.driver.find_element(By.XPATH, '//textarea[@name="cards"]')

       #writes the cards to the textbox
        for card in deckList:
            textarea.send_keys(card + Keys.RETURN)

        #remormat date in matchRecord
        #reformats the date
        x, y, z = date.split('/')
        date = z + '/' + y + '/' + x

        #sets date, so deck possibilites from after that game aren't considered (as they don't exist at the time of playing)
        self.driver.find_element(By.XPATH, '//input[@name="date_end"]').send_keys(date)

        #clicks the submit button of the form
        self.driver.find_element(By.XPATH, '//td[@colspan="2"]/input[@type="submit"]').click()



    def clearCookieBanner(self):

        #if cookie banner present, click it, as it obstructs webdriver's view
        try:
            self.driver.find_element(By.XPATH, '//*[@id="cookie_window"]/div[2]/button').click()
        except:
            pass



    def getDeckNames(self):
        deckNames = []
        
        #gets number of decks on page
        decks = len(self.driver.find_elements(By.XPATH, '//td[@class="S12"]'))/3
        
        #if there are no decks on page, then return unknown as deckname, and quit DriverController() 
        if decks < 1:
            return 'unknown', None
        
        #sets number of decks to 5, if not under 5, so as to reduce time taken
        if decks > 5:
            decks = 5

        #loops through all decks on the page and gets their and name
        for deck in range(2, int(decks)+2):
            deckNames.append(self.driver.find_element(By.XPATH, f'//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{deck}]/td[2]/a').text)

        return deckNames



    def quit(self):
        
        #stops the driver
        self.driver.quit()



    def refactorDecklist(self):
        cards = {}
        
        for game in self.deckLists:
            for card in game:

                #may need to make start val 1

                #if the card isn't in the dictionary, then it's added with a value of 0
                #if it already exists, then it's vlaue is increased by 1
                #this value represents the number of the same card
                try:
                    cards[card] = cards[card]+1
                except:
                    cards[card] = 1
        
        #deckLists is no longer required
        del self.deckLists

        #return self.bubbleSort(cardVals)
        return cards
        


    def getDictNames(self, deckNames):
        
        #creates a dictionary of deckNames
        dictNames = {deckName:0 for deckName in deckNames}

        #gets number of decks with same name
        for deckName in deckNames:
            dictNames[deckName] = dictNames[deckName] + 1
        
        #gets percentage chance of said deck
        for deckName in dictNames:
            dictNames[deckName] = dictNames[deckName] / len(deckNames)

        return dictNames



if __name__ == "__main__":
    dc = DriverController(None, (("Fatal Push", "Fatal Push", "Swamp", "Thraben Inspector"), ("Plains", "Swamp", "Fatal Push"), ()), "02/02/2016")
    dc.startup()
    dc.returnDictNames()
    dc.quit()
