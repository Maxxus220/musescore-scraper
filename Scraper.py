from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
import shutil

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

# driver options
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

# initialize chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://musescore.com/user/16006641/scores/4197961")

# select div containing sheet music
body = driver.find_element(By.TAG_NAME, "body")
song_window = driver.find_element(By.ID, "jmuse-scroller-component")
song_window.click()
time.sleep(0.5)

score_num = 0

# load all pages by scrolling till bottom of div is reached searching for new scores each time
last_height = driver.execute_script("return document.getElementById(\"jmuse-scroller-component\").scrollTop")
while True:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    scores = driver.find_elements(By.CLASS_NAME, 'Hn_kk')
    print(len(scores))
    for score in scores:
        src = score.get_attribute('src')
        if 'score_' + str(score_num) in src:
            print(src)
            score_num+=1
    new_height = driver.execute_script("return document.getElementById(\"jmuse-scroller-component\").scrollTop")
    if new_height == last_height:
        break
    last_height = new_height
    
# scores = driver.find_elements(By.TAG_NAME, 'img')
# print(len(scores))
# for score in scores:
#     src = score.get_attribute('src')
#     print(src)
    # print(src)
    # r = requests.get(src, stream=True)
    # if r.status_code == 200:
    #     r.raw.decode_content = True
    #     with open("score", 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)

time.sleep(3)
driver.quit()