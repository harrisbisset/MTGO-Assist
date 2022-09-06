from ast import Return
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

gameNo = 1
date = "04/09/2022"
MB = ("Thalia, Guardian of Thraben", "Archon of Emeria")
SB = ("Mindbreak Trap", "Leyline of The Void")
format = "Vintage"
driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))


def main():

    driver.get("https://mtgtop8.com/search")
    select_element = driver.find_element(By.CSS_SELECTOR, 'select[name="format"]')
    select_object = Select(select_element)
    select_object.select_by_visible_text(format)

    if gameNo > 1:
        driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()
        addCards(MB + SB)
    else:
        addCards(MB)

    dateTo = driver.find_element(By.XPATH, '//input[@name="date_end"]')
    dateTo.send_keys(date)

    dateTo = driver.find_element(By.XPATH, '//td[@colspan="2"]//input[@type="submit"]').click()
    driver.implicitly_wait(3)

    deckListings = driver.find_element(By.XPATH, '//form[@name="compare_decks"]')
    decks = deckListings.find_elements(By.XPATH, '//td[@class="hover_tr"]')
    for currentDeck in decks:
        getRecord()
    driver.quit(currentDeck)

def addCards(cards):
    textarea = driver.find_element(By.XPATH, '//textarea[@name="cards"]')
    for listCard in range(0, len(cards)-1):
        textarea.send_keys(cards[listCard])
        textarea.send_keys(Keys.RETURN)


def getRecord(currentDeck):
    deck = currentDeck.find_elements(By.XPATH, '//td[@class="S12"]')
    deckName = deck.getText()
    deck.click()
    decklist = []
    cards = driver.find_elements(By.XPATH, '//div[@class="deck_line hover_tr"]')
    for card in cards:
        card.getText()
        decklist.append(card)

    #send to DB
    return

main()
