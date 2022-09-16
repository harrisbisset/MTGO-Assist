from ast import Return
from tkinter import E
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (ElementNotVisibleException,ElementNotSelectableException)
from selenium.common.exceptions import TimeoutException, NoSuchElementException


gameNo = 1
date = "04/09/2022"
MB = ("Thalia, Guardian of Thraben", "Archon of Emeria")
SB = ("Mindbreak Trap", "Leyline of The Void")
format = "Vintage"


class DriverController():
    def __init__(self):
        driverOptions = webdriver.ChromeOptions()
        driverOptions.add_argument('--ignore-certificate-errors')
        driverOptions.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=driverOptions)


    def get_site(self):
        self.driver.get("https://mtgtop8.com/search")


    def inputFormData(self, date, MB, SB, format):        
        select_element = self.driver.find_element(By.CSS_SELECTOR, 'select[name="format"]')
        select_object = Select(select_element)
        select_object.select_by_visible_text(format)

        #click cookie banner
        self.driver.find_element(By.XPATH, '//*[@id="cookie_window"]/div[2]/button').click()

        if gameNo > 1:
            cards = MB
        else:
            cards = MB + SB

        self.driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()
        textarea = self.driver.find_element(By.XPATH, '//textarea[@name="cards"]')
        for listCard in range(0, len(cards)-1):
            textarea.send_keys(cards[listCard])
            textarea.send_keys(Keys.RETURN)

        dateTo = self.driver.find_element(By.XPATH, '//input[@name="date_end"]')
        dateTo.send_keys(date)
        dateTo = self.driver.find_element(By.XPATH, '//td[@colspan="2"]//input[@type="submit"]').click()
        print("clicked")
        url = self.driver.current_url

        return url


    def getRecord(self, currentDeck, url):
        print('getting record')

        self.driver.get(url)
        print(url)#ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException]

        WebDriverWait(self.driver, timeout=5).until(lambda d: d.find_element(By.XPATH,f"//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{currentDeck}]/td[2]/a"))

        deckLink = self.driver.find_element(By.XPATH, f"//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{currentDeck}]/td[2]/a")
        # try:
        #     wait = WebDriverWait(self.driver,3)
        #     element = wait.until(EC.presence_of_element_located((By.XPATH, '//html/body/div/div/div[2]/div[1]/div[1]/a/img')))
        # except Exception as nse:
        #     print(nse)
        #     print("-----")
        #     print(str(nse))
        #     print("-----")
        #     print(nse.args)
        #     print("=====")
        #     self.driver.quit()
        # else:
        #     pass
        # finally:
        #     pass

        deckName = deckLink.text

        #update to driver.get
        urlDeck = deckLink.get_attribute('href')
        print(urlDeck)
        self.driver.get(urlDeck)

        #WebDriverWait(self.driver, timeout=7, poll_frequency=5, ignored_exceptions=[ElementNotVisibleException,ElementNotSelectableException]).until(EC.element_to_be_clickable((By.XPATH, "//html/body/div/div/div[2]/div[1]/div[1]/a")), 'Timed out waiting for element')
        try:
            WebDriverWait(self.driver, timeout=3, poll_frequency=5, ignored_exceptions=[ElementNotVisibleException]).until(EC.element_to_be_clickable((By.XPATH, '//html/body/div/div/div[2]/div[1]/div[1]/a/img')), 'Timed out waiting for element')
        except NoSuchElementException as nse:
            print(nse)
            print("-----")
            print(str(nse))
            print("-----")
            print(nse.args)
            print("=====")
        #deck = currentDeck.find_elements(By.XPATH, '//td[@class="S12"]')
        #deckName = deck.getText()
        decklist = []
        cards = self.driver.find_elements(By.XPATH, '//span[@class="L14"]')
        for card in cards:
            card = card.text
            decklist.append(card)
            
        print(decklist)
        print(deckName)

    
    def quit(self):
        self.driver.quit()







if __name__ == "__main__":
    dc = DriverController()
    dc.get_site()
    url = dc.inputFormData(date, MB, SB, format)
    for currentDeck in range(2,25):
        dc.getRecord(currentDeck, url)
    
    dc.quit()
