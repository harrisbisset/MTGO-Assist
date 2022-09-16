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
driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument('--ignore-certificate-errors')
driverOptions.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=driverOptions)


def main():

    driver.get("https://mtgtop8.com/search")
    select_element = driver.find_element(By.CSS_SELECTOR, 'select[name="format"]')
    select_object = Select(select_element)
    select_object.select_by_visible_text(format)

    #click cookie banner
    driver.find_element(By.XPATH, '//*[@id="cookie_window"]/div[2]/button').click()

    if gameNo > 1:
        cards = MB
    else:
        cards = MB + SB

    driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()
    textarea = driver.find_element(By.XPATH, '//textarea[@name="cards"]')
    for listCard in range(0, len(cards)-1):
        textarea.send_keys(cards[listCard])
        textarea.send_keys(Keys.RETURN)

    dateTo = driver.find_element(By.XPATH, '//input[@name="date_end"]')
    dateTo.send_keys(date)
    dateTo = driver.find_element(By.XPATH, '//td[@colspan="2"]//input[@type="submit"]').click()
    print("clicked")
    url = driver.current_url
    print(url)

    for currentDeck in range(2,25):
        print('before url')
        driver.get(url)
        print('url')
        getRecord(currentDeck)
    
    print(h)
    driver.quit()


# def addCards(cards):
#     textarea = driver.find_element(By.XPATH, '//textarea[@name="cards"]')
#     for listCard in range(0, len(cards)-1):
#         textarea.send_keys(cards[listCard])
#         textarea.send_keys(Keys.RETURN)


def getRecord(currentDeck):
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH,f"//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{currentDeck}]/td[2]/a"))
    deckLink = driver.find_element(By.XPATH, f"//body/div/div/table/tbody/tr/td[2]/form/table/tbody/tr[{currentDeck}]/td[2]/a")
    deckName = deckLink.text
    urlDeck = deckLink.get_attribute('href')
    print(urlDeck)
    driver.get(urlDeck)
    decklist = []
    cards = driver.find_elements(By.XPATH, '//div[@class="deck_line hover_tr"]')
    for card in cards:
        card = card.text
        decklist.append(card)
        print(card)

    #send to DB

main()
