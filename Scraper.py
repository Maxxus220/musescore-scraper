from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PIL import Image
from PyPDF2 import PdfMerger

import os
import time
import requests
import shutil

import tkinter as tk

def requestURL():
    return input("Enter a musescore url: ")

def requestSaveName():
    return input("Enter a name to save the song under: ")

# detects if score is svg or png
def detectScoreType(scoreUrl):
    if 'svg' in scoreUrl:
        return 'svg'
    elif 'png' in scoreUrl:
        return 'png'
    else:
        return None
    
# downloads png or svg then converts to pdf
def downloadScore(src, saveName):
    scoreType = detectScoreType(src)
    
    # download file
    r = requests.get(src, stream=True)
    if r.status_code == 200 or scoreType == None:
        r.raw.decode_content = True
        with open('./Music/' + saveName + '_' + str(score_num) + '.' + scoreType, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            f.close()
            
            # svg to pdf
            if scoreType == 'svg':
                svg = svg2rlg('./Music/' + saveName + '_' + str(score_num) + '.' + scoreType)
                renderPDF.drawToFile(svg, './Music/' + saveName + '_' + str(score_num) + '.pdf')
                os.remove('./Music/' + saveName + '_' + str(score_num) + '.' + scoreType)
            
            # png to pdf
            elif scoreType == 'png':
                png = Image.open('./Music/' + saveName + '_' + str(score_num) + '.' + scoreType)
                png = png.convert('RGB')
                png.save('./Music/' + saveName + '_' + str(score_num) + '.pdf')
                png.close()
                os.remove('./Music/' + saveName + '_' + str(score_num) + '.' + scoreType)
            
        print(saveName + '_' + str(score_num) + '.pdf successfully downloaded')
    else:
        print('Problem encountered while trying to download ' + saveName + str(score_num))
        
# takes singular score pages and converts them to a single pdf under saveName + '.pdf'
def mergePages(saveName, score_num):
    merger = PdfMerger()
    
    # add pages
    for i in range(0, score_num):
        merger.append('./Music/' + saveName + '_' + str(i) + '.pdf')
        
    merger.write('./Music/' + saveName + '.pdf')
    merger.close()
    
    # remove single pdfs
    for i in range(0, score_num):
        os.remove('./Music/' + saveName + '_' + str(i) + '.pdf')
        
    print('PDFs merged')
    
# source: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter user: Honest Abe
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    
# runs selenium, scrapes site for sheetmusic, and downloads sheetmusic as pdfs
def runScraper(url, saveName):
    
    if url == "" or saveName == "":
        return
    
    # driver options
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    # initialize chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

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
        
        # check for score elements
        scores = driver.find_elements(By.CLASS_NAME, 'Hn_kk')
        
        # check for next score
        for score in scores:
            src = score.get_attribute('src')
            if 'score_' + str(score_num) in src:
                downloadScore(src, saveName)
                score_num+=1
                
        # check for end of scrolling
        new_height = driver.execute_script("return document.getElementById(\"jmuse-scroller-component\").scrollTop")
        if new_height == last_height:
            break
        last_height = new_height
        
    mergePages(saveName, score_num)

    input('Press ENTER to quit')
    driver.quit()
    
window = tk.Tk()
window.geometry("500x300")
window.title("Musescore Scraper")
center(window)

url_label = tk.Label(text="Enter a Musescore url")
url_label.place(x = 100, y = 30, width=300)

url_entry = tk.Entry(width=100)
url_entry.place(x = 100, y = 50, width=300)

saveName_label = tk.Label(text="Enter a name to save the song under")
saveName_label.place(x = 100, y = 90, width = 300)

saveName_entry = tk.Entry()
saveName_entry.place(x = 100, y = 110, width=300)

submit_button = tk.Button(text="Download")
submit_button.bind('<Button>', lambda event, url=url_entry.get(), saveName=saveName_entry.get(): self.runScraper(url, saveName))
submit_button.place(x=200, y = 240, width=100)

window.mainloop()

#url = requestURL()
#saveName = requestSaveName()

