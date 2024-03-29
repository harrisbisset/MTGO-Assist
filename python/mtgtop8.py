from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


class DriverController():
    def __init__(self):
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



    def returnDeckName(self, deckLists, date):
        #calls the 'getSite()' method to open the url through the driver
        self.getSite()

        #calls the 'cookieBanner()' method to try and clear the cookie banner
        self.clearCookieBanner()

        #calls the 'inputFormData()' method to get all decks to be scraped
        self.inputFormData(deckLists['P1'][0], date)

        #gets the deck urls and names from the 'getDeckUrls()' method
        deckNames = self.getDeckNames()

        #if there are no decks found, then return deckNames (will have value of 'unknown')
        if deckNames == 'unknown':
            deckNames = {'NA', 1.0}
        else:
            #calls getDeckName() to create a dictionary of deckNames and %
            dictNames = self.getDictNames(deckNames)

        return dictNames, deckLists



    def getSite(self):
        self.driver.get(self.url)



    def inputFormData(self, deckList, date):

        #includes cards found in games played so far, as the what cards were sideboarded or not is impossible to find out
        self.driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()

        #loops through the list of cards, writing each card into the <textarea>
        textarea = self.driver.find_element(By.XPATH, '//textarea[@name="cards"]')

        #writes the cards to the textbox
        for card in deckList:
            textarea.send_keys(card + Keys.RETURN)

        #sets date, so deck possibilites from after that game aren't considered (as they don't exist at the time of playing)
        self.driver.find_element(By.XPATH, '//input[@name="date_end"]').send_keys(date['date'])

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
            return 'unknown'
        
        #sets number of decks to 5, if not under 5, so as to reduce time taken
        if decks > 5:
            decks = 5

        #loops through all decks on the page and gets their and name
        for deck in range(2, int(decks)+2):
            deckNames.append(self.driver.find_element(By.XPATH, f'//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{deck}]/td[2]/a').text)

        return deckNames



    def quitDc(self):
        
        #stops the driver
        self.driver.quit()

        


    def getDictNames(self, deckNames):
        
        #creates a dictionary of deckNames
        dictNames = {'deckNames':[{deckName:0 for deckName in deckNames}]}

        #gets number of decks with same name
        for deckName in deckNames:
            dictNames['deckNames'][0][deckName] = dictNames['deckNames'][0][deckName] + 1
        
        #gets percentage chance of said deck
        for deckName in dictNames['deckNames'][0]:
            dictNames['deckNames'][0][deckName] = dictNames['deckNames'][0][deckName] / len(deckNames)

        return dictNames
