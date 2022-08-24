from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import time

# def requestURL():
#     return input("Enter a musescore url: ")

# def requestSaveName():
#     return input("Enter a name to save the song under: ")

# def scrape():
#     driver = webdriver.Chrome()
#     driver.get("http://selenium.dev")
#     time.sleep(3)
#     driver.quit()

# url = requestURL()
# saveName = requestSaveName()
# scrape()

WINDOW_SIZE = "1920,1080"
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://musescore.com/user/16006641/scores/4197961")

body = driver.find_element(By.TAG_NAME, "body")
song_window = driver.find_element(By.ID, "jmuse-scroller-component")
song_window.click()
time.sleep(0.5)

last_height = driver.execute_script("return document.getElementById(\"jmuse-scroller-component\").scrollTop")
while True:
    
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    new_height = driver.execute_script("return document.getElementById(\"jmuse-scroller-component\").scrollTop")
    print(str(last_height) + ' | ' + str(new_height))
    if new_height == last_height:
        break
    last_height = new_height
    
time.sleep(3)
driver.quit()