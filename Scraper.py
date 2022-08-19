from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
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
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_options)
driver.get("http://selenium.dev")
time.sleep(3)
driver.quit()