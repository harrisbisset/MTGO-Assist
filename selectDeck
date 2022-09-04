from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select

gameNo = 1
date = "04/09/2022"
MB = "Card1, Card2"
SB = "Card3, Card4"


driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))

driver.get("https://mtgtop8.com/search")
select_element = driver.find_element(By.CSS_SELECTOR, 'select[name="format"]')
select_object = Select(select_element)
select_object.select_by_visible_text('Legacy')

textarea = driver.find_element(By.XPATH, '//textarea[@name="cards"]')
if gameNo > 1:
    driver.find_element(By.XPATH, '//input[@name="SB_check"]').click()
    textarea.send_keys(MB + SB)
else:
    textarea.send_keys(MB)

dateTo = driver.find_element(By.XPATH, '//input[name="date_end"]')
dateTo.send_keys(date)

dateTo = driver.find_element(By.XPATH, '//td[@colspan="2"]//input[@type="submit"]').click()
driver.implicitly_wait(3)

driver.quit()

